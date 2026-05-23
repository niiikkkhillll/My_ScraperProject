import asyncio
import re
import urllib.parse
import random
import sys
import json
from playwright.async_api import async_playwright

async def scrape_real_playwright(category: str, area: str, limit: int = 5, on_progress=None):
    # If on Windows and using an event loop other than ProactorEventLoop (e.g. SelectorEventLoop),
    # run Playwright inside a separate thread with a dedicated ProactorEventLoop to avoid NotImplementedError.
    if sys.platform == 'win32':
        current_loop = asyncio.get_event_loop()
        proactor_class = getattr(asyncio, 'ProactorEventLoop', None)
        if proactor_class is None or not isinstance(current_loop, proactor_class):
            def thread_wrapper():
                asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    return loop.run_until_complete(
                        _scrape_real_playwright_impl(category, area, limit, on_progress)
                    )
                finally:
                    loop.close()
            
            return await asyncio.to_thread(thread_wrapper)

    return await _scrape_real_playwright_impl(category, area, limit, on_progress)

async def _scrape_real_playwright_impl(category: str, area: str, limit: int = 5, on_progress=None):
    query = f"{category} in {area}"
    items = []
    
    try:
        if on_progress:
            await on_progress(5, "[INFO] Launching Chromium browser via Playwright Async API...")
            
        async with async_playwright() as p:
            # Launch browser with stealth and bot evasion details
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-blink-features=AutomationControlled"
                ]
            )
        
            context = await browser.new_context(
                viewport={"width": 1280, "height": 800},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/120.0.0.0 Safari/537.36",
                ignore_https_errors=True
            )
        
            page = await context.new_page()
        
            query_escaped = urllib.parse.quote_plus(query)
            search_url = f"https://www.google.com/maps/search/{query_escaped}"
        
            if on_progress:
                await on_progress(10, f"[INFO] Navigating directly to Maps search URL...")
            
            try:
                await page.goto(search_url, wait_until="domcontentloaded", timeout=60000)
            except Exception as nav_error:
                if on_progress:
                    await on_progress(18, f"[WARNING] Search navigation timed out, continuing anyway...")
            await page.wait_for_timeout(5000)

            # Dismiss common Google cookie/dialog banners that block the page
            try:
                buttons = await page.query_selector_all('button')
                for btn in buttons:
                    try:
                        text = (await btn.inner_text()).strip().lower()
                        if text in ['accept all', 'continue', 'agree', 'i agree', 'accept']:
                            await btn.click()
                            await page.wait_for_timeout(1200)
                            break
                    except Exception:
                        continue
            except Exception:
                pass

            if on_progress:
                await on_progress(20, "[INFO] Waiting for search results to render...")
            
            # Wait for result cards or links to load
            try:
                await page.wait_for_selector("div[role='feed'], a[href*='/maps/place/'], a[href*='/place/']", timeout=45000)
            except Exception:
                if on_progress:
                    await on_progress(25, "[WARNING] Results did not appear quickly. Proceeding with best effort...")

            if on_progress:
                await on_progress(28, f"[INFO] Scrolling results sidebar to discover up to {limit} listings...")
            
            # Scroll sidebar container
            scroll_count = 0
            place_links = []
            required_discover = limit + 25
            max_scrolls = max(35, required_discover // 2)
        
            while scroll_count < max_scrolls:
                # Extract links
                anchors = await page.eval_on_selector_all(
                    "a[href*='/maps/place/'], a[href*='/place/'], a[aria-label][href*='/maps/']",
                    "nodes => nodes.map(a => ({ name: a.getAttribute('aria-label') || '', url: a.href }))"
                )
            
                # De-duplicate
                seen_names = set()
                unique_links = []
                for item in anchors:
                    item_name_clean = item["name"].strip().lower()
                    if item_name_clean not in seen_names and item["name"]:
                        seen_names.add(item_name_clean)
                        unique_links.append(item)
            
                place_links = unique_links
            
                if on_progress:
                    progress_step = min(28 + int((scroll_count / max_scrolls) * 22), 50)
                    await on_progress(progress_step, f"[SCROLLING] Loaded {len(place_links)} lead listings...")
                
                if len(place_links) >= required_discover:
                    if on_progress:
                        await on_progress(50, f"[SUCCESS] Discovered enough listings ({len(place_links)}). Proceeding to details...")
                    break
                
                # Scroll down
                await page.evaluate(
                    """() => {
                        const feed = document.querySelector('div[role="feed"]') || 
                                     document.querySelector('.m6QErb.D3DuXb') ||
                                     document.querySelector('div[style*="overflow-y: auto"]');
                        if (feed) {
                            feed.scrollTo(0, feed.scrollHeight);
                        } else {
                            window.scrollBy(0, 1000);
                        }
                    }"""
                )
            
                await asyncio.sleep(2.5)
            
                # Check if end of list is reached
                end_reached = await page.evaluate(
                    """() => {
                        const elements = Array.from(document.querySelectorAll('span, div'));
                        const endSpan = elements.find(el => el.innerText && el.innerText.includes("reached the end of the list"));
                        if (!endSpan) return false;
                        const rect = endSpan.getBoundingClientRect();
                        return rect.width > 0 && rect.height > 0;
                    }"""
                )
                if end_reached:
                    if on_progress:
                        await on_progress(48, "[INFO] Reached the end of Google Maps results list.")
                    break
                
                scroll_count += 1
            
            if not place_links:
                if on_progress:
                    await on_progress(40, "[ERROR] No Google Maps place links found. The page may be blocked or selectors may be wrong.")
                raise Exception("No Google Maps place links were found for this query. The page may be blocked or the selector has changed.")
            if on_progress:
                await on_progress(52, f"[INFO] Performing deep profile parsing to get {limit} unique leads...")
            
            # Extract individual business data interactively on the same page
            for i, link in enumerate(place_links):
                if len(items) >= limit:
                    break
                
                progress_step = 52 + int((len(items) / limit) * 43)
                if on_progress:
                    await on_progress(progress_step, f"[EXTRACTING] [{len(items)+1}/{limit}] Fetching details for: '{link['name']}'...")
                
                try:
                    # Find and click the link in the left panel to load details
                    # Prefer exact-href matches, then aria-label matches, then fall back to indexed anchor
                    escaped_url = link["url"].replace("'", "\\'")
                    a_element = None

                    try:
                        # Try exact href match first (handles full URLs)
                        a_element = await page.query_selector(f"a[href='{escaped_url}']")
                    except Exception:
                        a_element = None

                    # If exact href not found, try to locate among all candidate anchors and match by href or aria-label
                    if not a_element:
                        candidates = await page.query_selector_all("a[href*='/maps/place/'], a[href*='/place/'], a[aria-label][href*='/maps/']")
                        if candidates:
                            found = None
                            for idx_h, handle in enumerate(candidates):
                                try:
                                    href = await handle.get_attribute('href') or ''
                                    aria = await handle.get_attribute('aria-label') or ''
                                except Exception:
                                    href = ''
                                    aria = ''

                                # Normalize and compare
                                try:
                                    norm_href = href.split('?')[0]
                                    norm_link = link['url'].split('?')[0]
                                except Exception:
                                    norm_href = href
                                    norm_link = link.get('url', '')

                                if norm_link and (norm_link in norm_href or norm_href in norm_link):
                                    found = idx_h
                                    break
                                if link.get('name') and link['name'].strip().lower() and link['name'].strip().lower() in aria.strip().lower():
                                    found = idx_h
                                    break

                            if found is not None:
                                a_element = candidates[found]
                            else:
                                # As a last resort, pick by position: use the same index as the link list when possible
                                try:
                                    idx_choice = i if i < len(candidates) else len(candidates) - 1
                                    a_element = candidates[idx_choice]
                                    if on_progress:
                                        await on_progress(progress_step, f"[WARNING] Using positional fallback anchor for '{link.get('name','')}' (index {idx_choice}).")
                                except Exception:
                                    a_element = None

                    # Additional aria-label / button fallbacks if no anchor found
                    if not a_element and link.get('name'):
                        escaped_name = link["name"].replace("'", "\\'")
                        a_element = await page.query_selector(f"a[aria-label*='{escaped_name}'], div[role='link'][aria-label*='{escaped_name}'], button[aria-label*='{escaped_name}']")
                
                    if a_element:
                        await a_element.scroll_into_view_if_needed()
                    
                        # Get the currently displayed business name before clicking
                        prev_header = await page.evaluate("""() => {
                            let nameEl = document.querySelector('h1.DUwDvf');
                            if (!nameEl) {
                                const h1s = Array.from(document.querySelectorAll('h1'));
                                nameEl = h1s.find(el => el.innerText.trim().toLowerCase() !== 'results' && el.innerText.trim() !== '');
                            }
                            return nameEl ? nameEl.innerText.trim() : '';
                        }""")
                    
                        # Click using direct DOM method (100% reliable)
                        await page.evaluate("(el) => el.click()", a_element)
                    
                        # Wait dynamically for the header to change
                        pane_updated = False
                        for _ in range(8):
                            curr_header = await page.evaluate("""() => {
                                let nameEl = document.querySelector('h1.DUwDvf');
                                if (!nameEl) {
                                    const h1s = Array.from(document.querySelectorAll('h1'));
                                    nameEl = h1s.find(el => el.innerText.trim().toLowerCase() !== 'results' && el.innerText.trim() !== '');
                                }
                                return nameEl ? nameEl.innerText.trim() : '';
                            }""")
                            if curr_header and curr_header != prev_header:
                                pane_updated = True
                                break
                            await asyncio.sleep(0.5)
                        
                        if not pane_updated:
                            # Fallback native force-click
                            try:
                                await a_element.click(force=True, timeout=3000)
                                await asyncio.sleep(2.0)
                            except:
                                pass
                    else:
                        if on_progress:
                            await on_progress(progress_step, f"[WARNING] Anchor element not found for '{link.get('name','')}', skipping this item.")
                        raise Exception("Anchor element not found in list")
                
                    # Fetch details
                    details = await page.evaluate(
                        r"""(url) => {
                            let nameEl = document.querySelector('h1.DUwDvf');
                            if (!nameEl) {
                                const h1s = Array.from(document.querySelectorAll('h1'));
                                // Find an h1 that doesn't say 'Results'
                                nameEl = h1s.find(el => el.innerText.trim().toLowerCase() !== 'results' && el.innerText.trim() !== '');
                            }
                            const name = nameEl ? nameEl.innerText.trim() : '';
                        
                            let rating = 0;
                            let reviewsCount = 0;
                            const starsEl = document.querySelector('div.F7nice') || document.querySelector('.F7nice');
                            if (starsEl) {
                                const starsText = starsEl.innerText || '';
                                const match = starsText.match(/([0-9.]+)\s*\(([0-9,]+)\)/);
                                if (match) {
                                    rating = parseFloat(match[1]);
                                    reviewsCount = parseInt(match[2].replace(/,/g, ''), 10);
                                } else {
                                    const parts = starsText.split('(');
                                    if (parts.length >= 2) {
                                        rating = parseFloat(parts[0].trim());
                                        reviewsCount = parseInt(parts[1].replace(')', '').replace(/,/g, '').trim(), 10);
                                    }
                                }
                            }
                        
                const addressEl = document.querySelector('button[data-item-id="address"]') || document.querySelector('[aria-label*="Address"]') || document.querySelector('[data-item-id*="address"]');
                            const address = addressEl ? addressEl.innerText.trim() : '';
                        
const phoneEl = document.querySelector('button[data-item-id^="phone:"]') ||
                            document.querySelector('a[href^="tel:"]') ||
                            document.querySelector('button[aria-label*="Call"]') ||
                            document.querySelector('button[aria-label*="phone"]') ||
                            document.querySelector('button[aria-label*="Phone"]') ||
                            document.querySelector('[aria-label*="Phone"]');
                        const phone = phoneEl ? phoneEl.innerText.trim() : '';
                        
                        // Robust website detection: try multiple strategies to find valid website URL
                        let website = '';
                        let websiteMethod = 'none';
                        try {
                            // Method 1: Explicit authority/website button (most reliable)
                            let sel = document.querySelector('a[data-item-id="authority"]');
                            if (sel && sel.href) { 
                                website = sel.href;
                                websiteMethod = 'authority-button';
                            }
                            
                            // Method 2: Try common website label patterns
                            if (!website) {
                                sel = document.querySelector('a[aria-label*="Website"], a[aria-label*="website"], a[aria-label*="Visit website"]');
                                if (sel && sel.href) { 
                                    website = sel.href;
                                    websiteMethod = 'aria-label-website';
                                }
                            }
                            
                            // Method 3: Search for external links in info section or any non-google domain
                            if (!website) {
                                const allLinks = Array.from(document.querySelectorAll('a[href*="http"]'));
                                // Filter: exclude google, maps, and take first valid domain
                                const candidates = allLinks.filter(a => {
                                    const h = a.href || '';
                                    return h && !h.includes('google.com') && !h.includes('/maps/') && !h.includes('maps.google');
                                });
                                
                                // Prefer links with website/visit/official in text or aria-label
                                const labeled = candidates.find(a => {
                                    const t = (a.innerText || a.getAttribute('aria-label') || '').toLowerCase();
                                    return /website|visit|official|home/.test(t);
                                });
                                if (labeled && labeled.href) {
                                    website = labeled.href;
                                    websiteMethod = 'labeled-link';
                                } else if (candidates.length > 0) {
                                    website = candidates[0].href;
                                    websiteMethod = 'first-external-link';
                                }
                            }
                            
                            // Method 4: Search entire page for any domain-like URL not in google
                            if (!website) {
                                const pageLinks = Array.from(document.querySelectorAll('a'));
                                const external = pageLinks.find(a => {
                                    const h = a.href || '';
                                    try {
                                        const url = new URL(h);
                                        return url.hostname && !url.hostname.includes('google.com') && !url.hostname.includes('maps.google');
                                    } catch(e) { return false; }
                                });
                                if (external && external.href) {
                                    website = external.href;
                                    websiteMethod = 'page-external-link';
                                }
                            }
                        } catch (e) {
                            website = '';
                            websiteMethod = 'error';
                        }
                        
                        // Return website and method for debugging
                        return { name, rating, reviewsCount, address, phone, website, websiteMethod, latitude: 0, longitude: 0 };
                        
                        
                            let latitude = 0;
                            let longitude = 0;
                            const urlMatch = url.match(/!3d(-?[0-9.]+)!4d(-?[0-9.]+)/);
                            if (urlMatch) {
                                latitude = parseFloat(urlMatch[1]);
                                longitude = parseFloat(urlMatch[2]);
                            } else {
                                const coordMatch = url.match(/@(-?[0-9.]+),(-?[0-9.]+)/);
                                if (coordMatch) {
                                    latitude = parseFloat(coordMatch[1]);
                                    longitude = parseFloat(coordMatch[2]);
                                }
                            }
                        
                            return { name, rating, reviewsCount, address, phone, website, websiteMethod, latitude, longitude };
                        }""",
                        link["url"]
                    )
                
                    # Clean details
                    extracted_name = details["name"]
                    clean_name = extracted_name if (extracted_name and extracted_name.lower() != "results") else link["name"]
                
                    # Log website extraction method for debugging
                    website_method = details.get("websiteMethod", "unknown")
                    if on_progress:
                        if details.get("website"):
                            await on_progress(progress_step, f"[DEBUG] Item '{clean_name}': website found via {website_method}")
                        else:
                            await on_progress(progress_step, f"[DEBUG] Item '{clean_name}': NO website found (method: {website_method})")
                
                    def clean_field(val: str) -> str:

                        if not val:
                            return ""
                        # Split by newline, strip Private Use Area icons (E000-F8FF) and join
                        lines = [line.strip() for line in val.split('\n') if line.strip()]
                        cleaned_lines = []
                        for line in lines:
                            cleaned = ''.join(c for c in line if not (0xE000 <= ord(c) <= 0xF8FF)).strip()
                            if cleaned:
                                cleaned_lines.append(cleaned)
                        return " ".join(cleaned_lines)
                
                    cleaned_address = clean_field(details["address"]) or "Address not listed"
                    cleaned_phone = clean_field(details["phone"]) or "Phone not listed"
                    cleaned_website = details["website"] or "No website listed"
                
                    # Enrich from Website
                    real_email = None
                    real_phone = None
                    clean_name_slug = re.sub(r'[^a-z0-9]', '', clean_name.lower())
                    if cleaned_website and cleaned_website != "No website listed":
                        site_page = None
                        try:
                            async def do_enrichment():
                                nonlocal real_email, real_phone, site_page
                                site_page = await context.new_page()
                            
                                # Block images, stylesheets, media, and fonts to load pages 10x faster and prevent timeouts
                                async def intercept(route):
                                    try:
                                        if route.request.resource_type in ["image", "stylesheet", "media", "font"]:
                                            await route.abort()
                                        else:
                                            await route.continue_()
                                    except:
                                        pass
                                await site_page.route("**/*", intercept)
                            
                                await site_page.goto(cleaned_website, wait_until="domcontentloaded", timeout=15000)
                            
                                # Extract tel and mailto links directly from DOM (100% accurate)
                                tel_hrefs = await site_page.evaluate("""() => {
                                    const anchors = Array.from(document.querySelectorAll('a[href^="tel:"]'));
                                    return anchors.map(a => a.getAttribute('href').replace('tel:', '').trim());
                                }""")
    
                                mailto_hrefs = await site_page.evaluate("""() => {
                                    const anchors = Array.from(document.querySelectorAll('a[href^="mailto:"]'));
                                    return anchors.map(a => a.getAttribute('href').replace('mailto:', '').split('?')[0].trim());
                                }""")
    
                                # Extract visible text and JSON-LD scripts (often contain structured contact info)
                                page_texts = await site_page.evaluate("""() => {
                                    const body = document.body ? document.body.innerText : '';
                                    const ld = Array.from(document.querySelectorAll('script[type="application/ld+json"]')).map(s => s.innerText || '');
                                    const metas = Array.from(document.querySelectorAll('meta[name], meta[property]')).map(m => (m.getAttribute('content')||''));
                                    return { body, ld, metas, hostname: location.hostname };
                                }""")
    
                                # Email Extraction: prefer mailto links, then JSON-LD/meta/body regexes.
                                # Also prefer non-generic business addresses (avoid info@, contact@, etc.)
                                generic_prefixes = ('info@', 'contact@', 'admin@', 'hello@', 'support@', 'no-reply@', 'noreply@', 'enquiry@', 'webmaster@', 'office@', 'sales@')
    
                                # Start with explicit mailto links
                                candidates = []
                                for m in mailto_hrefs:
                                    if m and '@' in m:
                                        candidates.append(m)
    
                                # Combine body, LD-JSON and meta content for regex searching
                                combined_text = ''
                                try:
                                    combined_text = (page_texts.get('body') or '') + '\n' + '\n'.join(page_texts.get('ld') or []) + '\n' + '\n'.join(page_texts.get('metas') or [])
                                    page_hostname = (page_texts.get('hostname') or '').lower()
                                    visible_text = page_texts.get('body') or ''
                                except Exception:
                                    combined_text = ''
                                    page_hostname = ''
                                    visible_text = ''
    
                                # Regex-scan combined_text for email-like tokens
                                emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', combined_text)
                                # Filter out obvious asset filenames that accidentally match
                                emails = [e.strip() for e in emails if not e.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.css', '.js', '.svg', '.webp'))]
                                for e in emails:
                                    if e and e not in candidates:
                                        candidates.append(e)
    
                                # Try to parse JSON-LD blocks for explicit email fields
                                try:
                                    for ld_text in (page_texts.get('ld') or []):
                                        try:
                                            parsed = json.loads(ld_text)
                                        except Exception:
                                            continue
    
                                        # Recursively find email-like values inside JSON-LD
                                        def find_emails(obj):
                                            found = []
                                            if isinstance(obj, dict):
                                                for k, v in obj.items():
                                                    if isinstance(v, (dict, list)):
                                                        found += find_emails(v)
                                                    elif isinstance(v, str):
                                                        if re.match(r'.+@.+\..+', v):
                                                            found.append(v.strip())
                                            elif isinstance(obj, list):
                                                for item in obj:
                                                    found += find_emails(item)
                                            return found
    
                                        for em in find_emails(parsed):
                                            if em and em not in candidates:
                                                candidates.append(em)
                                except Exception:
                                    pass
    
                                # Deduplicate while preserving order
                                seen_e = set()
                                uniq_cands = []
                                for e in candidates:
                                    le = e.lower()
                                    if le not in seen_e:
                                        seen_e.add(le)
                                        uniq_cands.append(e)
    
                                # Prefer non-generic addresses
                                non_generic = [e for e in uniq_cands if not any(e.lower().startswith(p) for p in generic_prefixes)]
                                chosen = None
                                if non_generic:
                                    # Prefer address whose domain matches the site hostname
                                    for e in non_generic:
                                        try:
                                            domain = e.split('@',1)[1].lower()
                                            if page_hostname and page_hostname in domain:
                                                chosen = e
                                                break
                                        except Exception:
                                            pass
                                    if not chosen:
                                        chosen = non_generic[0]
                                elif uniq_cands:
                                    # Fallback to first candidate (may be generic)
                                    chosen = uniq_cands[0]
    
                                # If chosen is missing or generic-only, attempt contact page lookup before closing the tab
                                if not chosen or (chosen and any(chosen.lower().startswith(p) for p in generic_prefixes)):
                                    try:
                                        # find contact links on the site
                                        contact_links = await site_page.evaluate("""() => {
                                            const anchors = Array.from(document.querySelectorAll('a'));
                                            return anchors.map(a => ({ href: a.href || '', text: (a.innerText || a.getAttribute('aria-label') || '') })).filter(o => o.href && /contact|contact-us|contactus|get-in-touch|support/i.test(o.href + ' ' + o.text));
                                        }""")
    
                                        seen_hrefs = set()
                                        for c in contact_links:
                                            href = c.get('href')
                                            if not href or href in seen_hrefs:
                                                continue
                                            seen_hrefs.add(href)
                                            try:
                                                await site_page.goto(href, wait_until='domcontentloaded', timeout=8000)
                                            except Exception:
                                                pass
    
                                            try:
                                                mailtos2 = await site_page.evaluate("""() => Array.from(document.querySelectorAll('a[href^=\"mailto:\"]')).map(a=>a.getAttribute('href').replace('mailto:','').split('?')[0].trim())""")
                                            except Exception:
                                                mailtos2 = []
                                            try:
                                                contact_text = await site_page.evaluate("() => document.body ? document.body.innerText : ''")
                                            except Exception:
                                                contact_text = ''
    
                                            contact_emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', contact_text)
                                            for e in mailtos2 + contact_emails:
                                                if e and e not in uniq_cands:
                                                    uniq_cands.append(e)
                                                    if not any(e.lower().startswith(p) for p in generic_prefixes):
                                                        chosen = e
                                                        break
                                            if chosen:
                                                break
    
                                        if not chosen and uniq_cands:
                                            non_generic2 = [e for e in uniq_cands if not any(e.lower().startswith(p) for p in generic_prefixes)]
                                            if non_generic2:
                                                chosen = non_generic2[0]
                                            else:
                                                chosen = uniq_cands[0]
                                    except Exception:
                                        pass
    
                                if chosen:
                                    real_email = chosen
                                    
                                clean_tels = [re.sub(r'\D', '', t) for t in tel_hrefs if len(re.sub(r'\D', '', t)) >= 10]
                                if clean_tels:
                                    real_phone = urllib.parse.unquote(tel_hrefs[0])
                                else:
                                    # Search in visible text (Indian phone number formats: e.g. 079-12345678, +91 98250 30555, 9825030555)
                                    phone_matches = re.findall(r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}', visible_text)
                                    valid_phones = [p.strip() for p in phone_matches if len(re.sub(r'\D', '', p)) >= 10]
                                    filtered_phones = []
                                    for p in valid_phones:
                                        digits = re.sub(r'\D', '', p)
                                        # Indian mobile starts with 6,7,8,9
                                        if len(digits) == 10 and digits[0] in '6789':
                                            filtered_phones.append(p)
                                        elif len(digits) == 11 and digits.startswith('0') and digits[1] in '6789':
                                            filtered_phones.append(p)
                                        elif len(digits) >= 11 and digits.startswith('91') and len(digits) <= 13:
                                            filtered_phones.append(p)
                                        elif '079' in p or '79' in p:
                                            filtered_phones.append(p)
                                    if filtered_phones:
                                        real_phone = filtered_phones[0]
                                    elif valid_phones:
                                        real_phone = valid_phones[0]
                            
                            # Enforce a strict 25-second timeout on the entire website parsing task
                            await asyncio.wait_for(do_enrichment(), timeout=25.0)
                        except Exception as web_err:
                            if on_progress:
                                await on_progress(progress_step, f"[WARNING] Website enrichment timed out or failed for {cleaned_website}: {str(web_err)}")
                        finally:
                            if site_page:
                                try:
                                    await site_page.close()
                                except:
                                    pass
                            
                    email = real_email if real_email else "N/A"
                    final_phone = real_phone if real_phone else cleaned_phone
                
                    # Strict final deduplication
                    normalized_name = clean_name.strip().lower()
                    if normalized_name in [item["name"].strip().lower() for item in items]:
                        continue
                
                    items.append({
                        "id": len(items) + 1,
                        "name": clean_name,
                        "rating": details["rating"] or 0,
                        "reviewsCount": details["reviewsCount"] or 0,
                        "category": category.capitalize(),
                        "address": cleaned_address,
                        "phone": final_phone,
                        "website": cleaned_website,
                        "email": email,
                        "socials": {
                            "facebook": "",
                            "instagram": ""
                        },
                        "latitude": details["latitude"],
                        "longitude": details["longitude"]
                    })

                except Exception as e:
                    if on_progress:
                        await on_progress(progress_step, f"[WARNING] Skipping failed details extraction for '{link['name']}': {str(e)}")
                    continue

                await asyncio.sleep(1.0)

            if on_progress:
                await on_progress(98, "[INFO] Scraping completed. Closing browser connections...")
            
            await browser.close()
        
            if on_progress:
                await on_progress(100, "[SUCCESS] Playwright maps scraping finished completely!")
            
            return items
        
    except Exception as outer_error:
        import traceback
        traceback.print_exc()
        if on_progress:
            await on_progress(95, f"[ERROR] Real Playwright scraper failed: {repr(outer_error)}")
            await on_progress(100, f"[INFO] Returning {len(items)} records extracted before error.")
        
        if not items:
            raise outer_error
        # Return partial results if any were collected
        return items

def random_decision(probability: float) -> bool:
    return random.random() < probability
