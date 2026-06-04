/**
 * Outscraper Clone - Google Maps Scraper (app.js)
 * Fully functional: tag inputs, location autocomplete, Get Data button, polling, results table
 */

(function () {
  'use strict';

  // ─── Location Suggestions Database ──────────────────────────
  var LOCATIONS = [
    // Indian States
    { label: 'Andhra Pradesh', sub: 'State, India' },
    { label: 'Arunachal Pradesh', sub: 'State, India' },
    { label: 'Assam', sub: 'State, India' },
    { label: 'Bihar', sub: 'State, India' },
    { label: 'Chhattisgarh', sub: 'State, India' },
    { label: 'Goa', sub: 'State, India' },
    { label: 'Gujarat', sub: 'State, India' },
    { label: 'Haryana', sub: 'State, India' },
    { label: 'Himachal Pradesh', sub: 'State, India' },
    { label: 'Jharkhand', sub: 'State, India' },
    { label: 'Karnataka', sub: 'State, India' },
    { label: 'Kerala', sub: 'State, India' },
    { label: 'Madhya Pradesh', sub: 'State, India' },
    { label: 'Maharashtra', sub: 'State, India' },
    { label: 'Manipur', sub: 'State, India' },
    { label: 'Meghalaya', sub: 'State, India' },
    { label: 'Mizoram', sub: 'State, India' },
    { label: 'Nagaland', sub: 'State, India' },
    { label: 'Odisha', sub: 'State, India' },
    { label: 'Punjab', sub: 'State, India' },
    { label: 'Rajasthan', sub: 'State, India' },
    { label: 'Sikkim', sub: 'State, India' },
    { label: 'Tamil Nadu', sub: 'State, India' },
    { label: 'Telangana', sub: 'State, India' },
    { label: 'Tripura', sub: 'State, India' },
    { label: 'Uttar Pradesh', sub: 'State, India' },
    { label: 'Uttarakhand', sub: 'State, India' },
    { label: 'West Bengal', sub: 'State, India' },
    // Major Cities
    { label: 'Ahmedabad', sub: 'City, Gujarat, India' },
    { label: 'Surat', sub: 'City, Gujarat, India' },
    { label: 'Vadodara', sub: 'City, Gujarat, India' },
    { label: 'Rajkot', sub: 'City, Gujarat, India' },
    { label: 'Mumbai', sub: 'City, Maharashtra, India' },
    { label: 'Pune', sub: 'City, Maharashtra, India' },
    { label: 'Nagpur', sub: 'City, Maharashtra, India' },
    { label: 'Delhi', sub: 'City, Delhi, India' },
    { label: 'New Delhi', sub: 'Capital, Delhi, India' },
    { label: 'Bangalore', sub: 'City, Karnataka, India' },
    { label: 'Bengaluru', sub: 'City, Karnataka, India' },
    { label: 'Hyderabad', sub: 'City, Telangana, India' },
    { label: 'Chennai', sub: 'City, Tamil Nadu, India' },
    { label: 'Kolkata', sub: 'City, West Bengal, India' },
    { label: 'Jaipur', sub: 'City, Rajasthan, India' },
    { label: 'Lucknow', sub: 'City, Uttar Pradesh, India' },
    { label: 'Kanpur', sub: 'City, Uttar Pradesh, India' },
    { label: 'Noida', sub: 'City, Uttar Pradesh, India' },
    { label: 'Gurgaon', sub: 'City, Haryana, India' },
    { label: 'Chandigarh', sub: 'City, Punjab, India' },
    { label: 'Indore', sub: 'City, Madhya Pradesh, India' },
    { label: 'Bhopal', sub: 'City, Madhya Pradesh, India' },
    { label: 'Patna', sub: 'City, Bihar, India' },
    { label: 'Kochi', sub: 'City, Kerala, India' },
    { label: 'Coimbatore', sub: 'City, Tamil Nadu, India' },
    { label: 'Visakhapatnam', sub: 'City, Andhra Pradesh, India' },
    { label: 'Bhubaneswar', sub: 'City, Odisha, India' },
    { label: 'Guwahati', sub: 'City, Assam, India' },
    // Ahmedabad areas
    { label: 'Satellite, Ahmedabad', sub: 'Area, Gujarat, India' },
    { label: 'Navrangpura, Ahmedabad', sub: 'Area, Gujarat, India' },
    { label: 'Bopal, Ahmedabad', sub: 'Area, Gujarat, India' },
    { label: 'Prahlad Nagar, Ahmedabad', sub: 'Area, Gujarat, India' },
    { label: 'Vastrapur, Ahmedabad', sub: 'Area, Gujarat, India' },
    { label: 'Bodakdev, Ahmedabad', sub: 'Area, Gujarat, India' },
    { label: 'Maninagar, Ahmedabad', sub: 'Area, Gujarat, India' },
    { label: 'Chandkheda, Ahmedabad', sub: 'Area, Gujarat, India' },
    { label: 'Thaltej, Ahmedabad', sub: 'Area, Gujarat, India' },
    { label: 'Gota, Ahmedabad', sub: 'Area, Gujarat, India' },
    // Mumbai areas
    { label: 'Andheri, Mumbai', sub: 'Area, Maharashtra, India' },
    { label: 'Bandra, Mumbai', sub: 'Area, Maharashtra, India' },
    { label: 'Juhu, Mumbai', sub: 'Area, Maharashtra, India' },
    { label: 'Powai, Mumbai', sub: 'Area, Maharashtra, India' },
    { label: 'Worli, Mumbai', sub: 'Area, Maharashtra, India' },
    // US States
    { label: 'Alabama', sub: 'State, United States' },
    { label: 'Alaska', sub: 'State, United States' },
    { label: 'Arizona', sub: 'State, United States' },
    { label: 'Arkansas', sub: 'State, United States' },
    { label: 'California', sub: 'State, United States' },
    { label: 'Colorado', sub: 'State, United States' },
    { label: 'Florida', sub: 'State, United States' },
    { label: 'Georgia', sub: 'State, United States' },
    { label: 'Illinois', sub: 'State, United States' },
    { label: 'New York', sub: 'State, United States' },
    { label: 'Texas', sub: 'State, United States' },
    { label: 'Washington', sub: 'State, United States' },
    // US Cities
    { label: 'New York City', sub: 'City, New York, USA' },
    { label: 'Los Angeles', sub: 'City, California, USA' },
    { label: 'Chicago', sub: 'City, Illinois, USA' },
    { label: 'Houston', sub: 'City, Texas, USA' },
    { label: 'Phoenix', sub: 'City, Arizona, USA' },
    { label: 'Philadelphia', sub: 'City, Pennsylvania, USA' },
    { label: 'San Antonio', sub: 'City, Texas, USA' },
    { label: 'San Diego', sub: 'City, California, USA' },
    { label: 'Dallas', sub: 'City, Texas, USA' },
    { label: 'San Francisco', sub: 'City, California, USA' },
    // UK
    { label: 'London', sub: 'City, England, UK' },
    { label: 'Manchester', sub: 'City, England, UK' },
    { label: 'Birmingham', sub: 'City, England, UK' },
    { label: 'Leeds', sub: 'City, England, UK' },
    // UAE
    { label: 'Dubai', sub: 'City, UAE' },
    { label: 'Abu Dhabi', sub: 'City, UAE' },
    { label: 'Sharjah', sub: 'City, UAE' },
    // Australia
    { label: 'Sydney', sub: 'City, New South Wales, Australia' },
    { label: 'Melbourne', sub: 'City, Victoria, Australia' },
    { label: 'Brisbane', sub: 'City, Queensland, Australia' },
    { label: 'Perth', sub: 'City, Western Australia, Australia' },
    // Canada
    { label: 'Toronto', sub: 'City, Ontario, Canada' },
    { label: 'Vancouver', sub: 'City, British Columbia, Canada' },
    { label: 'Montreal', sub: 'City, Quebec, Canada' },
  ];

  // ─── State ──────────────────────────────────────────────────
  let categoryTags = [];
  let locationTags = [];
  let activeJobId  = null;
  let pollingTimer = null;
  let lastLogCount = 0;
  let activeSuggIdx = -1;

  // ─── DOM refs ────────────────────────────────────────────────
  const categoriesBox   = document.getElementById('categories-box');
  const categoryInput   = document.getElementById('category-input');
  const clearCatBtn     = document.getElementById('clear-categories');

  const locationTagsBox = document.getElementById('location-tags-box');
  const locationInput   = document.getElementById('location-input');
  const clearLocBtn     = document.getElementById('clear-locations');
  const countrySelect   = document.getElementById('country-select');
  const flagEl          = document.querySelector('.flag');

  const limitInput      = document.getElementById('input-limit');
  const btnGetData      = document.getElementById('btn-get-data');
  const btnSave         = document.getElementById('btn-save');
  const engineInput     = document.getElementById('input-engine');

  const progressCard    = document.getElementById('progress-card');
  const progressBarFill = document.getElementById('progress-bar');
  const progressPct     = document.getElementById('progress-pct');
  const logConsole      = document.getElementById('log-console');

  const resultsSection  = document.getElementById('results-section');
  const resultsTbody    = document.getElementById('results-tbody');
  const btnDownload     = document.getElementById('btn-download');
  const kpiTotal        = document.getElementById('kpi-total');
  const kpiRating       = document.getElementById('kpi-rating');
  const kpiPhone        = document.getElementById('kpi-phone');
  const kpiWeb          = document.getElementById('kpi-web');

  // ─── INIT ────────────────────────────────────────────────────
  renderCategoryTags();
  renderLocationTags();
  buildAutocompleteDropdown();

  // ─── ENGINE SELECTOR ─────────────────────────────────────────
  document.querySelectorAll('.engine-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var selectedEngine = this.dataset.engine;
      
      // Update button states
      document.querySelectorAll('.engine-btn').forEach(function (b) {
        b.classList.remove('active');
      });
      this.classList.add('active');
      
      // Update hidden input
      engineInput.value = selectedEngine;
    });
  });

  // Initialize the hidden engine input from the visible default button
  var activeEngineBtn = document.querySelector('.engine-btn.active');
  if (activeEngineBtn) {
    engineInput.value = activeEngineBtn.dataset.engine;
  } else {
    engineInput.value = 'real';
    var defaultRealBtn = document.querySelector('.engine-btn[data-engine="real"]');
    if (defaultRealBtn) defaultRealBtn.classList.add('active');
  }

  // ─── CATEGORY TAG INPUT ──────────────────────────────────────
  categoryInput.addEventListener('keydown', function (e) {
    if ((e.key === 'Enter' || e.key === ',') && this.value.trim()) {
      e.preventDefault();
      addCategoryTag(this.value.trim().replace(/,+$/, ''));
    }
    if (e.key === 'Backspace' && this.value === '' && categoryTags.length > 0) {
      categoryTags.pop();
      renderCategoryTags();
    }
  });

  // Click on the box focuses the hidden input
  categoriesBox.addEventListener('click', function () {
    categoryInput.focus();
  });

  clearCatBtn.addEventListener('click', function () {
    categoryTags = [];
    categoryInput.value = '';
    renderCategoryTags();
  });

  // Try chips for categories
  document.querySelectorAll('.try-chip:not(.location-chip)').forEach(function (btn) {
    btn.addEventListener('click', function () {
      addCategoryTag(this.dataset.value);
    });
  });

  function addCategoryTag(val) {
    if (!val || categoryTags.indexOf(val) !== -1) return;
    categoryTags.push(val);
    categoryInput.value = '';
    renderCategoryTags();
    categoryInput.focus();
  }

  function removeCategoryTag(index) {
    categoryTags.splice(index, 1);
    renderCategoryTags();
  }

  function renderCategoryTags() {
    // Remove all existing chips (keep only the input)
    Array.from(categoriesBox.querySelectorAll('.tag-chip')).forEach(function (c) { c.remove(); });

    categoryTags.forEach(function (tag, i) {
      var chip = document.createElement('span');
      chip.className = 'tag-chip';
      chip.innerHTML = escapeHtml(tag) + ' <span class="remove" data-idx="' + i + '">&#215;</span>';
      chip.querySelector('.remove').addEventListener('click', function (e) {
        e.stopPropagation();
        removeCategoryTag(parseInt(this.dataset.idx, 10));
      });
      categoriesBox.insertBefore(chip, categoryInput);
    });

    categoryInput.placeholder = categoryTags.length === 0 ? 'Select or enter categories' : '';
  }

  // ─── AUTOCOMPLETE DROPDOWN ───────────────────────────────────
  var dropdown;

  function buildAutocompleteDropdown() {
    dropdown = document.createElement('div');
    dropdown.id = 'location-dropdown';
    dropdown.style.cssText = [
      'position:absolute', 'background:#fff', 'border:1px solid #d1d5db',
      'border-radius:8px', 'box-shadow:0 8px 24px rgba(0,0,0,0.12)',
      'z-index:9999', 'max-height:280px', 'overflow-y:auto',
      'display:none', 'min-width:320px', 'font-size:13px'
    ].join(';');
    document.body.appendChild(dropdown);
  }

  function positionDropdown() {
    var rect = locationTagsBox.getBoundingClientRect();
    dropdown.style.top  = (rect.bottom + window.scrollY + 4) + 'px';
    dropdown.style.left = rect.left + 'px';
    dropdown.style.width = rect.width + 'px';
  }

  function showSuggestions(query) {
    if (!query || query.length < 1) { hideDropdown(); return; }
    var q = query.toLowerCase();
    var matches = LOCATIONS.filter(function (loc) {
      return loc.label.toLowerCase().indexOf(q) === 0 ||
             loc.label.toLowerCase().indexOf(' ' + q) !== -1;
    }).slice(0, 10);

    if (matches.length === 0) { hideDropdown(); return; }

    dropdown.innerHTML = '';
    activeSuggIdx = -1;
    matches.forEach(function (loc, i) {
      var item = document.createElement('div');
      item.style.cssText = 'display:flex;flex-direction:column;padding:10px 14px;cursor:pointer;border-bottom:1px solid #f3f4f6;transition:background 0.1s;';
      var highlighted = loc.label.replace(new RegExp('(' + escapeRegex(query) + ')', 'gi'), '<strong>$1</strong>');
      item.innerHTML =
        '<span style="color:#111;font-weight:500">' + highlighted + '</span>' +
        '<span style="color:#9ca3af;font-size:11.5px;margin-top:2px">' + loc.sub + '</span>';
      item.addEventListener('mouseenter', function () {
        clearHighlight();
        this.style.background = '#f3f4f6';
        activeSuggIdx = i;
      });
      item.addEventListener('mouseleave', function () { this.style.background = ''; });
      item.addEventListener('mousedown', function (e) {
        e.preventDefault();
        selectSuggestion(loc.label);
      });
      dropdown.appendChild(item);
    });

    positionDropdown();
    dropdown.style.display = 'block';
  }

  function clearHighlight() {
    Array.from(dropdown.children).forEach(function (c) { c.style.background = ''; });
  }

  function hideDropdown() {
    dropdown.style.display = 'none';
    activeSuggIdx = -1;
  }

  function selectSuggestion(val) {
    addLocationTag(val);
    locationInput.value = '';
    hideDropdown();
    locationInput.focus();
  }

  function escapeRegex(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  // ─── LOCATION TAG INPUT ──────────────────────────────────────
  locationInput.addEventListener('input', function () {
    showSuggestions(this.value.trim());
  });

  locationInput.addEventListener('keydown', function (e) {
    var items = dropdown.style.display !== 'none' ? Array.from(dropdown.children) : [];

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      clearHighlight();
      activeSuggIdx = Math.min(activeSuggIdx + 1, items.length - 1);
      if (items[activeSuggIdx]) items[activeSuggIdx].style.background = '#f3f4f6';
      return;
    }
    if (e.key === 'ArrowUp') {
      e.preventDefault();
      clearHighlight();
      activeSuggIdx = Math.max(activeSuggIdx - 1, 0);
      if (items[activeSuggIdx]) items[activeSuggIdx].style.background = '#f3f4f6';
      return;
    }
    if (e.key === 'Enter') {
      e.preventDefault();
      if (activeSuggIdx >= 0 && items[activeSuggIdx]) {
        var label = LOCATIONS.filter(function (l) {
          return items[activeSuggIdx].textContent.indexOf(l.label) === 0;
        })[0];
        if (label) { selectSuggestion(label.label); return; }
      }
      if (this.value.trim()) {
        addLocationTag(this.value.trim());
        hideDropdown();
      }
      return;
    }
    if (e.key === 'Escape') { hideDropdown(); return; }
    if (e.key === 'Backspace' && this.value === '' && locationTags.length > 0) {
      locationTags.pop();
      renderLocationTags();
    }
  });

  locationInput.addEventListener('blur', function () {
    setTimeout(hideDropdown, 150);
  });

  locationTagsBox.addEventListener('click', function () {
    locationInput.focus();
  });

  clearLocBtn.addEventListener('click', function () {
    locationTags = [];
    locationInput.value = '';
    renderLocationTags();
    hideDropdown();
  });

  // Country flag update
  var flagMap = {
    'United States': '🇺🇸', 'United Kingdom': '🇬🇧', 'India': '🇮🇳',
    'Canada': '🇨🇦', 'Australia': '🇦🇺', 'Germany': '🇩🇪',
    'France': '🇫🇷', 'UAE': '🇦🇪'
  };
  countrySelect.addEventListener('change', function () {
    if (flagEl && flagMap[this.value]) flagEl.textContent = flagMap[this.value];
  });

  // Try chips for locations
  document.querySelectorAll('.location-chip').forEach(function (btn) {
    btn.addEventListener('click', function () {
      addLocationTag(this.dataset.value);
    });
  });

  function addLocationTag(val) {
    if (!val || locationTags.indexOf(val) !== -1) return;
    locationTags.push(val);
    locationInput.value = '';
    renderLocationTags();
    locationInput.focus();
  }

  function removeLocationTag(index) {
    locationTags.splice(index, 1);
    renderLocationTags();
  }

  function renderLocationTags() {
    // Remove all existing tags and "+more" spans (keep only the input)
    Array.from(locationTagsBox.querySelectorAll('.location-tag, .location-more')).forEach(function (el) { el.remove(); });

    var visible = locationTags.slice(0, 5);
    var extra   = locationTags.length - visible.length;

    visible.forEach(function (tag, i) {
      var span = document.createElement('span');
      span.className = 'location-tag';
      span.dataset.val = tag;
      span.innerHTML = escapeHtml(tag) + ' <span class="tag-remove" data-idx="' + i + '">&#215;</span>';
      span.querySelector('.tag-remove').addEventListener('click', function (e) {
        e.stopPropagation();
        removeLocationTag(parseInt(this.dataset.idx, 10));
      });
      locationTagsBox.insertBefore(span, locationInput);
    });

    if (extra > 0) {
      var more = document.createElement('span');
      more.className = 'location-more';
      more.textContent = '+ ' + extra + ' ...';
      locationTagsBox.insertBefore(more, locationInput);
    }

    locationInput.placeholder = locationTags.length === 0 ? 'Add location...' : '';
  }

  // ─── ENRICHMENT TABS ─────────────────────────────────────────
  document.getElementById('tab-packs').addEventListener('click', function () {
    this.classList.add('active');
    document.getElementById('tab-services').classList.remove('active');
  });
  document.getElementById('tab-services').addEventListener('click', function () {
    this.classList.add('active');
    document.getElementById('tab-packs').classList.remove('active');
  });

  // ─── GET DATA BUTTON ─────────────────────────────────────────
  btnGetData.addEventListener('click', function () {
    var category = categoryTags.length > 0 ? categoryTags.join(', ') : categoryInput.value.trim();
    var area     = locationTags.length  > 0 ? locationTags.join(', ')  : countrySelect.value;
    var limit    = parseInt(limitInput.value, 10);
    if (isNaN(limit) || limit < 1) limit = 1;
    if (limit > 500) limit = 500;

    if (!category) {
      categoryInput.focus();
      categoriesBox.style.outline = '2px solid #ef4444';
      setTimeout(function () { categoriesBox.style.outline = ''; }, 2000);
      return;
    }

    startScrape(category, area, limit);
  });

  function startScrape(category, area, limit) {
    // Reset
    clearInterval(pollingTimer);
    activeJobId  = null;
    lastLogCount = 0;

    logConsole.innerHTML = '';
    updateProgress(0);
    resultsSection.classList.add('hidden');
    progressCard.classList.remove('hidden');
    progressCard.scrollIntoView({ behavior: 'smooth', block: 'start' });

    btnGetData.disabled = true;
    btnDownload.disabled = true;
    btnGetData.innerHTML = '<span style="display:inline-block;width:14px;height:14px;border:2px solid rgba(255,255,255,0.3);border-top-color:#fff;border-radius:50%;animation:spin 0.8s linear infinite;vertical-align:middle;margin-right:6px;"></span> Getting Data...';

    var engine = 'real';
    addLog('Sending request to Python backend...', 'cyan');
    addLog('Category: ' + category + ' | Area: ' + area + ' | Limit: ' + limit + ' | Engine: REAL', 'gray');

    var enrichEmail = document.getElementById('input-enrich-email').checked;
    fetch('/api/scrape', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ category: category, area: area, limit: limit, engine: engine, enrichEmail: enrichEmail })
    })
    .then(function (res) {
      if (!res.ok) return res.json().then(function (e) { throw new Error(e.detail || 'Request failed'); });
      return res.json();
    })
    .then(function (data) {
      activeJobId = data.jobId;
      addLog('Job created: ' + activeJobId, 'green');
      pollStatus(activeJobId);
    })
    .catch(function (err) {
      addLog('ERROR: ' + err.message, 'red');
      resetButton();
    });
  }

  function pollStatus(jobId) {
    pollingTimer = setInterval(function () {
      fetch('/api/scrape/status/' + jobId)
      .then(function (res) {
        if (!res.ok) throw new Error('Status fetch failed');
        return res.json();
      })
      .then(function (job) {
        updateProgress(job.progress);
        renderNewLogs(job.logs);

        if (job.status === 'completed') {
          clearInterval(pollingTimer);
          onComplete(job);
        } else if (job.status === 'failed') {
          clearInterval(pollingTimer);
          addLog('FAILED: ' + (job.error || 'Unknown error'), 'red');
          resetButton();
        }
      })
      .catch(function (err) {
        addLog('Poll error: ' + err.message, 'yellow');
      });
    }, 1000);
  }

  function onComplete(job) {
    updateProgress(100);
    addLog('Done! ' + job.results.length + ' records extracted.', 'green');
    resetButton();

    var results = job.results;
    var total   = results.length;
    var ratingSum = 0, ratingCnt = 0, phones = 0, websites = 0;

    results.forEach(function (r) {
      var rating = parseFloat(r.rating);
      if (!isNaN(rating) && rating > 0) { ratingSum += rating; ratingCnt++; }
      if (r.phone && r.phone !== 'N/A' && r.phone !== 'No phone listed') phones++;
      if (r.website && r.website !== 'N/A' && r.website !== 'No website listed') websites++;
    });

    kpiTotal.textContent  = total;
    kpiRating.textContent = ratingCnt > 0 ? '⭐ ' + (ratingSum / ratingCnt).toFixed(1) : '—';
    kpiPhone.textContent  = total > 0 ? Math.round((phones / total) * 100) + '%' : '0%';
    kpiWeb.textContent    = websites;

    // Build table
    resultsTbody.innerHTML = '';
    if (total === 0) {
      resultsTbody.innerHTML = '<tr><td colspan="9" style="text-align:center;color:#9ca3af;padding:30px;">No records found.</td></tr>';
    } else {
      results.forEach(function (item, idx) {
        var r = parseFloat(item.rating);
        var ratingHtml = '<span style="color:#9ca3af">N/A</span>';
        if (!isNaN(r) && r > 0) {
          var cls = r >= 4.0 ? 'rating-high' : r >= 3.0 ? 'rating-medium' : 'rating-low';
          ratingHtml = '<span class="rating-badge ' + cls + '">⭐ ' + r.toFixed(1) + '</span>';
        }
        var websiteHtml = (item.website && item.website !== 'N/A' && item.website !== 'No website listed')
          ? '<a href="' + item.website + '" target="_blank" rel="noopener">' + escapeHtml(item.website) + '</a>'
          : 'N/A';

        var tr = document.createElement('tr');
        tr.innerHTML =
          '<td>' + (idx + 1) + '</td>' +
          '<td><strong>' + escapeHtml(item.name || '') + '</strong></td>' +
          '<td>' + escapeHtml(item.category || 'N/A') + '</td>' +
          '<td>' + ratingHtml + '</td>' +
          '<td>' + (item.reviewsCount || 0) + '</td>' +
          '<td>' + escapeHtml(item.phone || 'N/A') + '</td>' +
          '<td>' + websiteHtml + '</td>' +
          '<td>' + escapeHtml(item.email || 'N/A') + '</td>' +
          '<td>' + escapeHtml(item.address || 'N/A') + '</td>';
        resultsTbody.appendChild(tr);
      });
    }

    activeJobId = job.id || activeJobId;
    btnDownload.disabled = false;
    btnDownload.onclick = function () {
      var downloadId = activeJobId || job.id;
      if (!downloadId) {
        addLog('Download failed: missing job id.', 'red');
        return;
      }
      window.location.href = '/api/download/' + encodeURIComponent(downloadId);
    };

    resultsSection.classList.remove('hidden');
    setTimeout(function () {
      resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 200);
  }

  // ─── Helpers ─────────────────────────────────────────────────
  function updateProgress(pct) {
    progressBarFill.style.width = pct + '%';
    progressPct.textContent     = pct + '%';
  }

  function addLog(msg, type) {
    var el = document.createElement('div');
    el.className = 'log-entry ' + (type || 'gray');
    var t = new Date();
    var ts = t.getHours() + ':' + pad(t.getMinutes()) + ':' + pad(t.getSeconds());
    el.textContent = '[' + ts + '] ' + msg;
    logConsole.appendChild(el);
    logConsole.scrollTop = logConsole.scrollHeight;
  }

  function renderNewLogs(logs) {
    for (var i = lastLogCount; i < logs.length; i++) {
      var text = logs[i];
      var type = 'gray';
      if (text.indexOf('[SUCCESS]') !== -1) type = 'green';
      else if (text.indexOf('[SCRAPING]') !== -1 || text.indexOf('[EXTRACTING]') !== -1) type = 'cyan';
      else if (text.indexOf('[ERROR]') !== -1 || text.indexOf('CRITICAL') !== -1) type = 'red';
      else if (text.indexOf('[WARNING]') !== -1) type = 'yellow';
      addLog(text, type);
    }
    lastLogCount = logs.length;
  }

  function resetButton() {
    btnGetData.disabled = false;
    btnGetData.innerHTML =
      '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">' +
      '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>' +
      '<polyline points="7 10 12 15 17 10"/>' +
      '<line x1="12" y1="15" x2="12" y2="3"/>' +
      '</svg> Get Data';
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function pad(n) { return n < 10 ? '0' + n : n; }

})();
