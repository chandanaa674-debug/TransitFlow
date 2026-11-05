
document.addEventListener("DOMContentLoaded", function () {

    // =========================================
    // 1. BUS STOP DATA
    // =========================================

    const locations = [
        "Statebank",
        "Hampankatta",
        "Mangaluru Central",
        "Bejai",
        "Kadri",
        "Kankanady"
    ];


    // =========================================
    // 2. BUS DATA
    // Demo data - replace with verified schedules
    // =========================================

    const buses = [
        {
            number: "RA001",
            name: "Demo Bus 01",
            operator: "Government",
            stops: [
                "Statebank",
                "Hampankatta",
                "Mangaluru Central"
            ],
            time: "08:00 AM",
            duration: "30 min",
            fare: 15
        },

        {
            number: "RA002",
            name: "Demo Bus 02",
            operator: "Private",
            stops: [
                "Statebank",
                "Bejai",
                "Kadri"
            ],
            time: "08:30 AM",
            duration: "40 min",
            fare: 20
        },

        {
            number: "RA003",
            name: "Demo Bus 03",
            operator: "Government",
            stops: [
                "Hampankatta",
                "Mangaluru Central",
                "Kankanady"
            ],
            time: "09:00 AM",
            duration: "35 min",
            fare: 18
        },

        {
            number: "RA004",
            name: "Demo Bus 04",
            operator: "Private",
            stops: [
                "Statebank",
                "Kankanady",
                "Kadri"
            ],
            time: "09:30 AM",
            duration: "50 min",
            fare: 25
        },

        {
            number: "RA005",
            name: "Demo Bus 05",
            operator: "Government",
            stops: [
                "Statebank",
                "Hampankatta",
                "Bejai"
            ],
            time: "10:00 AM",
            duration: "25 min",
            fare: 12
        }
    ];


    let currentResults = [];


    // =========================================
    // 3. SOURCE AND DESTINATION DROPDOWNS
    // =========================================

    const sourceSelect = document.getElementById("source");
    const destinationSelect = document.getElementById("destination");

    function populateLocations() {

        if (!sourceSelect || !destinationSelect) return;

        locations.forEach(location => {

            sourceSelect.add(
                new Option(location, location)
            );

            destinationSelect.add(
                new Option(location, location)
            );

        });
    }

    populateLocations();
    // NEARBY BUS STOPS

const nearbyButton = document.getElementById("nearbyButton");
const nearbyMessage = document.getElementById("nearbyMessage");
const nearbyResults = document.getElementById("nearbyResults");

nearbyButton.addEventListener("click", function () {

    nearbyMessage.textContent = "Getting your current location...";
    nearbyResults.innerHTML = "";

    if (!navigator.geolocation) {
        nearbyMessage.textContent =
            "Your browser does not support location access.";
        return;
    }

    navigator.geolocation.getCurrentPosition(

        function (position) {

            const userLat = position.coords.latitude;
            const userLng = position.coords.longitude;

            nearbyMessage.textContent =
                "Your location was detected! Finding nearby bus stops...";

            const nearbyStops = Object.entries(stopCoordinates)
                .map(([name, coordinates]) => {

                    const distance = calculateDistance(
                        userLat,
                        userLng,
                        coordinates[0],
                        coordinates[1]
                    );

                    return { name, distance };
                })
                .filter(stop => stop.distance <= 5)
                .sort((a, b) => a.distance - b.distance);

            if (nearbyStops.length === 0) {
                nearbyMessage.textContent =
                    "No demo bus stops found within 5 km.";
                return;
            }

            nearbyMessage.textContent = "Nearby bus stops:";

            nearbyResults.innerHTML = nearbyStops.map(stop => `
                <div class="nearby-card">
                    <h3>${stop.name}</h3>
                    <p>${stop.distance.toFixed(2)} km away</p>
                </div>
            `).join("");

        },

        function (error) {

            if (error.code === 1) {
                nearbyMessage.textContent =
                    "Location permission denied. Allow location in Chrome settings.";
            } else if (error.code === 2) {
                nearbyMessage.textContent =
                    "Your location is currently unavailable.";
            } else {
                nearbyMessage.textContent =
                    "Location request timed out. Please try again.";
            }

        },

        {
            enableHighAccuracy: true,
            timeout: 15000,
            maximumAge: 0
        }

    );

});


// DISTANCE CALCULATION

function calculateDistance(lat1, lon1, lat2, lon2) {

    const R = 6371;

    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;

    const a =
        Math.sin(dLat / 2) ** 2 +
        Math.cos(lat1 * Math.PI / 180) *
        Math.cos(lat2 * Math.PI / 180) *
        Math.sin(dLon / 2) ** 2;

    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    return R * c;
}


    // =========================================
    // 4. SWAP SOURCE AND DESTINATION
    // =========================================

    const swapButton = document.getElementById("swapButton");

    if (swapButton) {

        swapButton.addEventListener("click", function () {

            const temp = sourceSelect.value;

            sourceSelect.value = destinationSelect.value;

            destinationSelect.value = temp;

        });
    }


    // =========================================
    // 5. FIND DIRECT BUS ROUTES
    // =========================================

    function findDirectRoutes(source, destination) {

        return buses.filter(bus => {

            const sourceIndex = bus.stops.indexOf(source);

            const destinationIndex = bus.stops.indexOf(destination);

            return (
                sourceIndex !== -1 &&
                destinationIndex !== -1 &&
                sourceIndex < destinationIndex
            );

        });
    }


    // =========================================
    // 6. FIND CONNECTING BUS ROUTES
    // =========================================

    function findConnectingRoutes(source, destination) {

        const connectingRoutes = [];

        buses.forEach(firstBus => {

            const sourceIndex = firstBus.stops.indexOf(source);

            if (sourceIndex === -1) return;

            const possibleInterchanges =
                firstBus.stops.slice(sourceIndex + 1);

            possibleInterchanges.forEach(interchange => {

                buses.forEach(secondBus => {

                    if (firstBus.number === secondBus.number) return;

                    const interchangeIndex =
                        secondBus.stops.indexOf(interchange);

                    const destinationIndex =
                        secondBus.stops.indexOf(destination);

                    if (
                        interchangeIndex !== -1 &&
                        destinationIndex !== -1 &&
                        interchangeIndex < destinationIndex
                    ) {

                        connectingRoutes.push({
                            firstBus,
                            secondBus,
                            interchange,
                            totalFare: firstBus.fare + secondBus.fare,
                        estimatedMinutes:
                            parseInt(firstBus.duration) +
                            parseInt(secondBus.duration)
                        });

                    }

                });

            });

        });

        return connectingRoutes;
    }


    // =========================================
    // 7. CREATE BUS CARDS
    // =========================================

    function createBusCard(bus, connectingBus = null, interchange = "") {

        if (!connectingBus) {

            return `
                <div class="bus-card">

                    <span class="bus-number">
                        ${bus.number}
                    </span>

                    <h3>${bus.name}</h3>

                    <div class="bus-info">
                        <span>${bus.operator}</span>
                        <span>${bus.time}</span>
                    </div>

                    <div class="bus-stops">
                        <strong>Route:</strong>
                        ${bus.stops.join(" → ")}
                    </div>

                    <div class="bus-info">
                        <span>Duration: ${bus.duration}</span>
                        <span>Direct route</span>
                    </div>

                    <div class="bus-fare">
                        ₹${bus.fare}
                    </div>

                </div>
            `;
        }

        return `
            <div class="bus-card">

                <span class="bus-number">
                    CONNECTING ROUTE
                </span>

                <h3>
                    ${bus.name} + ${connectingBus.name}
                </h3>

                <div class="bus-info">
                    <span>${bus.time}</span>
                    <span>
                        ${bus.operator} + ${connectingBus.operator}
                    </span>
                </div>

                <div class="bus-stops">

                    <strong>First bus:</strong>
                    ${bus.stops.join(" → ")}

                    <br><br>

                    <strong>Change bus at:</strong>
                    ${interchange}

                    <br><br>

                    <strong>Second bus:</strong>
                    ${connectingBus.stops.join(" → ")}

                </div>

                <div class="bus-fare">
                    ₹${bus.fare + connectingBus.fare}
                </div>

            </div>
        `;
    }


    // =========================================
    // 8. DISPLAY BUS RESULTS
    // =========================================

    function displayResults(results) {

        const resultsContainer =
            document.getElementById("busResults");

        if (!resultsContainer) return;

        if (results.length === 0) {

            resultsContainer.innerHTML = `
                <div class="empty-state">
                    <h3>No buses found!</h3>
                    <p>
                        Try selecting another source or destination.
                    </p>
                </div>
            `;

            return;
        }

        resultsContainer.innerHTML = results.map(result => {

            return createBusCard(
                result.firstBus || result,
                result.secondBus || null,
                result.interchange || ""
            );

        }).join("");

    }


    // =========================================
    // 9. INTERACTIVE MAP - LEAFLET
    // =========================================

    // Approximate demo coordinates.
    // Verify actual bus stop coordinates before deployment.

    const stopCoordinates = {

        "Statebank": [12.8655, 74.8425],

        "Hampankatta": [12.8690, 74.8420],

        "Mangaluru Central": [12.8640, 74.8430],

        "Bejai": [12.8830, 74.8420],

        "Kadri": [12.8790, 74.8560],

        "Kankanady": [12.8560, 74.8560]

    };


    let routeMap = null;

    let routeLayer = null;

    let startMarker = null;

    let endMarker = null;


    // INITIALIZE THE MAP

    function initializeMap() {

        const mapElement =
            document.getElementById("routeMap");

        // Check if map section exists
        if (!mapElement) return;

        // Check whether Leaflet has loaded
        if (typeof L === "undefined") {

            console.error("Leaflet library is not loaded.");

            return;
        }

        // Create map
        routeMap = L.map("routeMap").setView(
            [12.8700, 74.8450],
            13
        );

        // Add OpenStreetMap tiles
        L.tileLayer(
            "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            {
                attribution:
                    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',

                maxZoom: 19
            }
        ).addTo(routeMap);

    }


    // DISPLAY SELECTED ROAD ROUTE

    async function showRoute(source, destination) {

        if (!routeMap) return;

        const start = stopCoordinates[source];

        const end = stopCoordinates[destination];

        if (!start || !end) {

            alert("Coordinates are not available for these stops.");

            return;
        }


        // Remove previous route

        if (routeLayer) {
            routeMap.removeLayer(routeLayer);
        }

        // Remove previous start marker

        if (startMarker) {
            routeMap.removeLayer(startMarker);
        }

        // Remove previous destination marker

        if (endMarker) {
            routeMap.removeLayer(endMarker);
        }


        const message =
            document.getElementById("mapMessage");

        if (message) {
            message.textContent = "Finding your route...";
        }


        try {

            // OSRM routing service
            const url =
                `https://router.project-osrm.org/route/v1/driving/` +
                `${start[1]},${start[0]};${end[1]},${end[0]}` +
                `?overview=full&geometries=geojson`;


            const response = await fetch(url);

            if (!response.ok) {

                throw new Error("Route service unavailable.");

            }


            const data = await response.json();

            if (
                !data.routes ||
                data.routes.length === 0
            ) {

                throw new Error("No route found.");

            }


            const route = data.routes[0];


            // Draw road route

            routeLayer = L.geoJSON(route.geometry, {

                style: {

                    color: "#C99B24",

                    weight: 6,

                    opacity: 0.9

                }

            }).addTo(routeMap);


            // Source marker

            startMarker = L.marker(start)

                .addTo(routeMap)

                .bindPopup(
                    `<b>Starting Point:</b> ${source}`
                );


            // Destination marker

            endMarker = L.marker(end)

                .addTo(routeMap)

                .bindPopup(
                    `<b>Destination:</b> ${destination}`
                );


            // Fit map to route

            routeMap.fitBounds(
                routeLayer.getBounds(),
                {
                    padding: [40, 40]
                }
            );


            // Calculate distance and driving duration

            const distance =
                (route.distance / 1000).toFixed(2);

            const duration =
                Math.round(route.duration / 60);


            if (message) {

                message.textContent =
                    `Route: ${source} to ${destination} | ` +
                    `Road distance: ${distance} km | ` +
                    `Estimated driving time: ${duration} minutes.`;

            }


        } catch (error) {

            console.error("Map error:", error);

            if (message) {

                message.textContent =
                    "Unable to load the road route. Please try again later.";

            }

        }

    }


    // INITIALIZE MAP ON PAGE LOAD

    initializeMap();


    // =========================================
    // 10. BUS SEARCH BUTTON
    // =========================================

    const searchButton =
        document.getElementById("searchButton");

    if (searchButton) {

        searchButton.addEventListener("click", function () {

            const source = sourceSelect.value;

            const destination = destinationSelect.value;


            // Validate selections

            if (!source || !destination) {

                alert("Please select both source and destination.");

                return;
            }


            if (source === destination) {

                alert("Source and destination cannot be the same.");

                return;
            }


            // Find direct routes

            const directRoutes =
                findDirectRoutes(source, destination);


            // UPDATE THE MAP

            showRoute(source, destination);


            // Find connecting routes

            const connectingRoutes =
                findConnectingRoutes(source, destination);


            // Combine both route types

            currentResults = [
                ...directRoutes,
                ...connectingRoutes
            ];


            // Display results

            displayResults(currentResults);

        });

    }


    // =========================================
    // 11. BUS FILTERS
    // =========================================

    const operatorFilter =
        document.getElementById("operatorFilter");

    const routeFilter =
        document.getElementById("routeFilter");


    function applyFilters() {

        let filtered = [...currentResults];


        // Operator filter

        if (
            operatorFilter &&
            operatorFilter.value !== "all"
        ) {

            filtered = filtered.filter(result => {

                const firstBus =
                    result.firstBus || result;

                return firstBus.operator === operatorFilter.value;

            });

        }


        // Direct and connecting route filter

        if (
            routeFilter &&
            routeFilter.value !== "all"
        ) {

            filtered = filtered.filter(result => {

                if (routeFilter.value === "direct") {

                    return !result.firstBus;

                }

                return Boolean(result.firstBus);

            });

        }


        displayResults(filtered);

    }


    if (operatorFilter) {

        operatorFilter.addEventListener(
            "change",
            applyFilters
        );

    }


    if (routeFilter) {

        routeFilter.addEventListener(
            "change",
            applyFilters
        );

    }


    // =========================================
    // 12. FEEDBACK FORM
    // =========================================

    const feedbackForm =
        document.getElementById("feedbackForm");


    if (feedbackForm) {

        feedbackForm.addEventListener(
            "submit",
            function (event) {

                event.preventDefault();


                const feedbackText =
                    document.getElementById("feedbackText")
                    .value.trim();


                if (!feedbackText) {

                    alert("Please enter your feedback.");

                    return;
                }


                const feedbacks = JSON.parse(

                    sessionStorage.getItem("raastaFeedback") || "[]"

                );


                feedbacks.push({

                    message: feedbackText,

                    date: new Date().toLocaleString()

                });


                sessionStorage.setItem(

                    "raastaFeedback",

                    JSON.stringify(feedbacks)

                );


                alert(
                    "Thank you! Your feedback has been submitted."
                );


                feedbackForm.reset();

            }
        );

    }


    // =========================================
    // 13. BUS DELAY REPORT FORM
    // =========================================

    const reportForm =
        document.getElementById("reportForm");


    if (reportForm) {

        reportForm.addEventListener(
            "submit",
            function (event) {

                event.preventDefault();


                const location =
                    document.getElementById("reportLocation")
                    .value.trim();


                const type =
                    document.getElementById("reportType").value;


                const description =
                    document.getElementById("reportDescription")
                    .value.trim();


                if (!location || !type || !description) {

                    alert("Please fill in all report details.");

                    return;
                }


                const reports = JSON.parse(

                    sessionStorage.getItem("raastaReports") || "[]"

                );


                reports.push({

                    location: location,

                    type: type,

                    description: description,

                    date: new Date().toLocaleString()

                });


                sessionStorage.setItem(

                    "raastaReports",

                    JSON.stringify(reports)

                );


                alert(
                    "Your report has been submitted successfully!"
                );


                reportForm.reset();

            }
        );

    }


    // =========================================
    // 14. ADMIN DASHBOARD
    // =========================================

    const adminBusRows =
        document.getElementById("adminBusRows");


    if (adminBusRows) {


        // Display bus information

        adminBusRows.innerHTML = buses.map(bus => `

            <tr>

                <td>${bus.number}</td>

                <td>${bus.name}</td>

                <td>${bus.operator}</td>

                <td>
                    ${bus.stops[0]}
                    →
                    ${bus.stops[bus.stops.length - 1]}
                </td>

                <td>${bus.time}</td>

            </tr>

        `).join("");


        // Get feedback and reports from session storage

        const reports = JSON.parse(

            sessionStorage.getItem("raastaReports") || "[]"

        );


        const feedbacks = JSON.parse(

            sessionStorage.getItem("raastaFeedback") || "[]"

        );


        const adminReports =
            document.getElementById("adminReports");

        const adminFeedback =
            document.getElementById("adminFeedback");


        // Display reports

        if (adminReports) {

            adminReports.innerHTML = reports.length

                ? reports.map(report => `

                    <p>

                        <strong>${report.location}</strong>

                        - ${report.type}

                        <br>

                        ${report.description}

                        <small>${report.date}</small>

                    </p>

                `).join("")

                : "<p>No delay reports submitted in this session.</p>";

        }


        // Display feedback

        if (adminFeedback) {

            adminFeedback.innerHTML = feedbacks.length

                ? feedbacks.map(feedback => `

                    <p>

                        ${feedback.message}

                        <small>${feedback.date}</small>

                    </p>

                `).join("")

                : "<p>No feedback submitted in this session.</p>";

        }


        // Update dashboard statistics

        const busCount =
            document.getElementById("busCount");

        const stopCount =
            document.getElementById("stopCount");

        const reportCount =
            document.getElementById("reportCount");

        const feedbackCount =
            document.getElementById("feedbackCount");


        if (busCount) {
            busCount.textContent = buses.length;
        }

        if (stopCount) {
            stopCount.textContent = locations.length;
        }

        if (reportCount) {
            reportCount.textContent = reports.length;
        }

        if (feedbackCount) {
            feedbackCount.textContent = feedbacks.length;
        }

    }


    // =========================================
    // 15. MOBILE NAVIGATION
    // =========================================

    const menuToggle =
        document.querySelector(".menu-toggle");

    const navLinks =
        document.querySelector(".nav-links");


    if (menuToggle && navLinks) {

        menuToggle.addEventListener("click", function () {

            navLinks.classList.toggle("show");

        });

    }
// ===================================
// RAASTA SCROLL JOURNEY ANIMATION
// ===================================


const roadProgress = document.getElementById("roadProgress");

function updateScrollJourney() {

    const scrollTop = window.scrollY;

    const maxScroll =
        document.documentElement.scrollHeight - window.innerHeight;

    const progress = maxScroll > 0
        ? Math.min(scrollTop / maxScroll, 1)
        : 0;

    if (movingBus && roadProgress) {

        movingBus.style.top = (progress * 100) + "%";

        roadProgress.style.height =
            (progress * 100) + "%";
    }
}

window.addEventListener("scroll", updateScrollJourney, {
    passive: true
});

window.addEventListener("resize", updateScrollJourney);

updateScrollJourney();


// ===================================
// SECTION REVEAL ANIMATION
// ===================================

const animatedSections = document.querySelectorAll(
    ".section, .hero, .welcome-banner"
);

animatedSections.forEach(section => {
    section.classList.add("reveal");
});

if ("IntersectionObserver" in window) {

    const revealObserver = new IntersectionObserver(
        (entries, observer) => {

            entries.forEach(entry => {

                if (entry.isIntersecting) {

                    entry.target.classList.add("visible");

                    observer.unobserve(entry.target);
                }

            });

        },
        {
            threshold: 0.12
        }
    );

    animatedSections.forEach(section => {
        revealObserver.observe(section);
    });

} else {

    animatedSections.forEach(section => {
        section.classList.add("visible");
    });

}

// RAASTA BUS SCROLL ANIMATION

const movingBus = document.getElementById("movingBus");


function updateBusAnimation() {

    if (!movingBus || !roadProgress) return;

    const scrollTop = window.scrollY;

    const maxScroll =
        document.documentElement.scrollHeight - window.innerHeight;

    const progress = maxScroll > 0
        ? Math.min(scrollTop / maxScroll, 1)
        : 0;

    movingBus.style.top = (progress * 100) + "%";

    roadProgress.style.height = (progress * 100) + "%";
}

window.addEventListener("scroll", updateBusAnimation, {
    passive: true
});

window.addEventListener("resize", updateBusAnimation);

updateBusAnimation();

});
