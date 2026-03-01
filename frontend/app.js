document.addEventListener('DOMContentLoaded', () => {
    const localities = ['Banashankari', 'Bannerghatta Road', 'Basavanagudi', 'Bellandur', 'Brigade Road', 'Brookefield', 'Btm', 'Church Street', 'Electronic City', 'Frazer Town', 'Hsr', 'Indiranagar', 'Jayanagar', 'Jp Nagar', 'Kalyan Nagar', 'Kammanahalli', 'Koramangala 4Th Block', 'Koramangala 5Th Block', 'Koramangala 6Th Block', 'Koramangala 7Th Block', 'Lavelle Road', 'Malleshwaram', 'Marathahalli', 'Mg Road', 'New Bel Road', 'Old Airport Road', 'Rajajinagar', 'Residency Road', 'Sarjapur Road', 'Whitefield'];
    const cuisinesList = ['Afghan', 'Afghani', 'African', 'American', 'Andhra', 'Arabian', 'Asian', 'Assamese', 'Australian', 'Awadhi', 'BBQ', 'Bakery', 'Bar Food', 'Belgian', 'Bengali', 'Beverages', 'Bihari', 'Biryani', 'Bohri', 'British', 'Bubble Tea', 'Burger', 'Burmese', 'Cafe', 'Cantonese', 'Charcoal Chicken', 'Chettinad', 'Chinese', 'Coffee', 'Continental', 'Desserts', 'Drinks Only', 'European', 'Fast Food', 'Finger Food', 'French', 'German', 'Goan', 'Greek', 'Grill', 'Gujarati', 'Healthy Food', 'Hot dogs', 'Hyderabadi', 'Ice Cream', 'Indian', 'Indonesian', 'Iranian', 'Italian', 'Japanese', 'Jewish', 'Juices', 'Kashmiri', 'Kebab', 'Kerala', 'Konkan', 'Korean', 'Lebanese', 'Lucknowi', 'Maharashtrian', 'Malaysian', 'Malwani', 'Mangalorean', 'Mediterranean', 'Mexican', 'Middle Eastern', 'Mithai', 'Modern Indian', 'Momos', 'Mongolian', 'Mughlai', 'Naga', 'Nepalese', 'North Eastern', 'North Indian', 'Oriya', 'Paan', 'Pan Asian', 'Parsi', 'Pizza', 'Portuguese', 'Rajasthani', 'Raw Meats', 'Roast Chicken', 'Rolls', 'Russian', 'Salad', 'Sandwich', 'Seafood', 'Sindhi', 'Singaporean', 'South American', 'South Indian', 'Spanish', 'Sri Lankan', 'Steak', 'Street Food', 'Sushi', 'Tamil', 'Tea', 'Tex-Mex', 'Thai', 'Tibetan', 'Turkish', 'Unknown', 'Vegan', 'Vietnamese', 'Wraps'];
    const cuisines = cuisinesList.filter(c => c !== 'Cafe' && c !== 'Unknown');

    const form = document.getElementById('recommendation-form');
    const resultsGrid = document.getElementById('results-section');
    const loading = document.getElementById('loading');
    const errorCard = document.getElementById('error-message');
    const errorText = document.getElementById('error-text');
    const submitBtn = document.getElementById('submit-btn');
    const localityCount = document.getElementById('locality-count');
    const cuisineCount = document.getElementById('cuisine-count');

    if (localityCount) localityCount.textContent = localities.length;
    if (cuisineCount) cuisineCount.textContent = cuisines.length;

    function hideAllDropdowns() {
        cityDropdown.classList.add('hidden');
        cuisineDropdown.classList.add('hidden');
        priceDropdown.classList.add('hidden');
        document.querySelectorAll('.form-group').forEach(fg => fg.classList.remove('active'));
    }

    const cityDisplay = document.getElementById('city-display');
    const cityDropdown = document.getElementById('city-dropdown');
    const cityOptions = document.getElementById('city-options');
    const citySearch = document.getElementById('city-search');
    let selectedCity = null;

    function renderCityOptions(filter = '') {
        cityOptions.innerHTML = '';
        const filtered = localities.filter(l => l.toLowerCase().includes(filter.toLowerCase()));

        if (filtered.length === 0) {
            const div = document.createElement('div');
            div.className = 'option-message';
            div.textContent = 'No localities found';
            cityOptions.appendChild(div);
            return;
        }

        filtered.forEach(l => {
            const div = document.createElement('div');
            div.className = `option ${selectedCity === l ? 'selected' : ''}`;
            div.textContent = l;
            div.addEventListener('click', (e) => {
                e.stopPropagation();
                selectedCity = l;
                updateCityDisplay();
                hideAllDropdowns();
            });
            cityOptions.appendChild(div);
        });
    }

    function updateCityDisplay() {
        if (selectedCity) {
            cityDisplay.innerHTML = `<span class="selected-tag">${selectedCity} <span class="remove">&times;</span></span>`;
            cityDisplay.querySelector('.remove').addEventListener('click', (e) => {
                e.stopPropagation();
                selectedCity = null;
                updateCityDisplay();
                renderCityOptions(citySearch.value);
            });
        } else {
            cityDisplay.innerHTML = `<span class="placeholder">Select locality...</span>`;
        }
    }

    cityDisplay.addEventListener('click', (e) => {
        e.stopPropagation();
        const isHidden = cityDropdown.classList.contains('hidden');
        hideAllDropdowns();
        if (isHidden) {
            citySearch.value = '';
            renderCityOptions();
            cityDropdown.classList.remove('hidden');
            cityDisplay.closest('.form-group').classList.add('active');
            setTimeout(() => citySearch.focus(), 50);
        }
    });

    citySearch.addEventListener('input', (e) => renderCityOptions(e.target.value));
    updateCityDisplay();
    renderCityOptions();

    const priceDisplay = document.getElementById('price-display');
    const priceDropdown = document.getElementById('price-dropdown');
    const priceOptions = document.getElementById('price-options');
    let selectedPrice = null;
    const priceMap = {
        'budget': 'Budget (₹ < 500)',
        'mid-range': 'Mid-range (₹500 - ₹1500)',
        'premium': 'Premium (₹ > 1500)'
    };

    function initPriceOptions() {
        priceOptions.querySelectorAll('.option').forEach(opt => {
            opt.addEventListener('click', (e) => {
                e.stopPropagation();
                selectedPrice = opt.dataset.val;
                updatePriceDisplay();

                // Update active state
                priceOptions.querySelectorAll('.option').forEach(o => o.classList.remove('selected'));
                opt.classList.add('selected');

                hideAllDropdowns();
            });
        });
    }

    function updatePriceDisplay() {
        if (selectedPrice) {
            priceDisplay.innerHTML = `<span class="selected-tag">${priceMap[selectedPrice]} <span class="remove">&times;</span></span>`;
            priceDisplay.querySelector('.remove').addEventListener('click', (e) => {
                e.stopPropagation();
                selectedPrice = null;
                updatePriceDisplay();

                // Unselect in list
                priceOptions.querySelectorAll('.option').forEach(o => o.classList.remove('selected'));
            });
        } else {
            priceDisplay.innerHTML = `<span class="placeholder">Select price range...</span>`;
        }
    }

    priceDisplay.addEventListener('click', (e) => {
        e.stopPropagation();
        const isHidden = priceDropdown.classList.contains('hidden');
        hideAllDropdowns();
        if (isHidden) {
            priceDropdown.classList.remove('hidden');
            priceDisplay.closest('.form-group').classList.add('active');
        }
    });

    initPriceOptions();

   
    const cuisineDisplay = document.getElementById('cuisine-display');
    const cuisineDropdown = document.getElementById('cuisine-dropdown');
    const cuisineOptions = document.getElementById('cuisine-options');
    const cuisineSearch = document.getElementById('cuisine-search');
    let selectedCuisines = [];

    function renderCuisineOptions(filter = '') {
        cuisineOptions.innerHTML = '';
        const filtered = cuisines.filter(c => c.toLowerCase().includes(filter.toLowerCase()));

        if (filtered.length === 0) {
            const div = document.createElement('div');
            div.className = 'option-message';
            div.textContent = 'No cuisines found';
            cuisineOptions.appendChild(div);
            return;
        }

        filtered.forEach(c => {
            const div = document.createElement('div');
            div.className = `option ${selectedCuisines.includes(c) ? 'selected' : ''}`;
            div.textContent = c;
            div.addEventListener('click', (e) => {
                e.stopPropagation();
                toggleCuisine(c);
            });
            cuisineOptions.appendChild(div);
        });
    }

    function toggleCuisine(c) {
        if (selectedCuisines.includes(c)) {
            selectedCuisines = selectedCuisines.filter(item => item !== c);
        } else {
            selectedCuisines.push(c);
        }
        updateCuisineDisplay();
        renderCuisineOptions(cuisineSearch.value);
    }

    function updateCuisineDisplay() {
        if (selectedCuisines.length === 0) {
            cuisineDisplay.innerHTML = '<span class="placeholder">Select cuisines...</span>';
        } else {
            cuisineDisplay.innerHTML = '';
            selectedCuisines.forEach(c => {
                const tag = document.createElement('span');
                tag.className = 'selected-tag';
                tag.innerHTML = `${c} <span class="remove" data-val="${c}">&times;</span>`;
                tag.querySelector('.remove').addEventListener('click', (e) => {
                    e.stopPropagation();
                    toggleCuisine(c);
                });
                cuisineDisplay.appendChild(tag);
            });
        }
    }

    cuisineDisplay.addEventListener('click', (e) => {
        e.stopPropagation();
        const isHidden = cuisineDropdown.classList.contains('hidden');
        hideAllDropdowns();
        if (isHidden) {
            cuisineSearch.value = '';
            renderCuisineOptions();
            cuisineDropdown.classList.remove('hidden');
            cuisineDisplay.closest('.form-group').classList.add('active');
            setTimeout(() => cuisineSearch.focus(), 50);
        }
    });

    cuisineSearch.addEventListener('input', (e) => renderCuisineOptions(e.target.value));
    renderCuisineOptions();

    document.addEventListener('click', () => {
        hideAllDropdowns();
    });

    [cityDropdown, cuisineDropdown, priceDropdown].forEach(el => {
        el.addEventListener('click', (e) => e.stopPropagation());
    });

    // Form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (!selectedCity) {
            showError('Locality is required! Please select a locality to continue.');
            return;
        }
        if (!selectedPrice) {
            showError('Price Range is required! Please select a price range to continue.');
            return;
        }

        resultsGrid.innerHTML = '';
        errorCard.classList.add('hidden');
        loading.classList.remove('hidden');
        submitBtn.disabled = true;

        const payload = {
            city: selectedCity,
            price_range: selectedPrice,
            cuisine: selectedCuisines.length > 0 ? selectedCuisines : null,
            min_rating: parseFloat(document.getElementById('min_rating').value) || 0
        };

        try {
            const response = await fetch('/api/recommend', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.detail || 'Failed to fetch recommendations');

            if (data.count === 0) {
                showError(data.message || 'No restaurants found matching your criteria.');
            } else {
                renderRecommendations(data.recommendations, data.ai_reasoning_summary);
            }
        } catch (err) {
            showError(err.message);
        } finally {
            loading.classList.add('hidden');
            submitBtn.disabled = false;
        }
    });

    function renderRecommendations(recommendations, summary) {
        if (summary) {
            const summaryDiv = document.createElement('div');
            summaryDiv.className = 'glass-card summary-card';
            summaryDiv.style.marginBottom = '30px';
            summaryDiv.style.gridColumn = '1 / -1';
            summaryDiv.style.borderLeft = '4px solid var(--accent-purple)';
            summaryDiv.innerHTML = `<p style="color: #e5e7eb; font-style: italic; font-size: 1.1rem;">${summary}</p>`;
            resultsGrid.appendChild(summaryDiv);
        }

        recommendations.forEach((rec, index) => {
            const card = document.createElement('div');
            card.className = 'glass-card restaurant-card';
            card.style.animationDelay = `${index * 0.1}s`;
            card.style.animation = 'fadeInUp 0.6s ease-out forwards';

            const cleanReasoning = rec.reasoning.replace(/Why you'll like it:/gi, '<strong>Why you\'ll like it:</strong>');

            card.innerHTML = `
                <div class="res-header">
                    <h3 class="res-name">${rec.name}</h3>
                    <span class="res-rating">${rec.rating} ★</span>
                </div>
                <div class="res-meta">
                    <p><i data-lucide="utensils"></i> ${rec.cuisines}</p>
                    <p><i data-lucide="banknote"></i> Avg. ₹${rec.average_cost} for two</p>
                    <p><i data-lucide="map-pin"></i> ${rec.address}</p>
                </div>
                <div class="res-reasoning">
                    ${cleanReasoning}
                </div>
            `;
            resultsGrid.appendChild(card);
        });

        if (window.lucide) window.lucide.createIcons();
    }

    function showError(message) {
        errorText.textContent = message;
        errorCard.classList.remove('hidden');
        errorCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
});
