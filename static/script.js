function loadData() {
  fetch('/api/data')
    .then(res => res.json())
    .then(data => {
      console.log("Data loaded:", data);

      // Combine the dataset with the latest input entry
      const fullData = [...data.dataset, data.latest];
      renderDashboard(fullData);
    })
    .catch(err => {
      console.error("Error loading data:", err);
      alert("Could not load data!");
    });
}

function renderDashboard(data) {
  const age = data.map(d => d.age);
  const retina = data.map(d => d.retina_thickness);
  const eyePressure = data.map(d => d.eye_pressure);
  const vision = data.map(d => d.vision_clarity);
  const sleep = data.map(d => d.sleep_hours);
  const bloodPressure = data.map(d => d.blood_pressure);
  const bloodSugar = data.map(d => d.blood_sugar);
  const screenTime = data.map(d => d.screen_time);
  const riskLevels = data.map(d => d.risk_level);
  const cornea = data.map(d => d.cornea_health);
  const cholesterol = data.map(d => d.cholesterol);

  const avg = arr => (arr.reduce((a, b) => a + b, 0) / arr.length).toFixed(2);

  document.getElementById("summary-cards").innerHTML = `
    <div class="card">Avg Eye Pressure<br><strong>${avg(eyePressure)}</strong></div>
    <div class="card">Avg Retina Thickness<br><strong>${avg(retina)}</strong></div>
    <div class="card">Avg Vision Clarity<br><strong>${avg(vision)}</strong></div>
    <div class="card">Avg Risk Level<br><strong>${avg(riskLevels)}</strong></div>
  `;

  createLineChart("retinaVsAgeChart", age, retina, "Retina Thickness", "#4B7BE5", true);
  createLineChart("eyePressureChart", age, eyePressure, "Eye Pressure", "#E74C3C", true);
  createLineChart("visionClarityChart", age, vision, "Vision Clarity", "#27AE60", true);
  createLineChart("bloodPressureChart", age, bloodPressure, "Blood Pressure", "#8E44AD", true);
  createLineChart("bloodSugarChart", age, bloodSugar, "Blood Sugar", "#D35400", true);
  createLineChart("corneaVsAgeChart", age, cornea, "Cornea Health", "#2ECC71", true);

  createBarChart("sleepVsRiskChart", sleep, riskLevels, "Risk Level", "#3498DB", false);
  createBarChart("cholesterolVsRiskChart", riskLevels, cholesterol, "Cholesterol", "#F39C12", false);
  createBarChart("screenTimeChart", riskLevels, screenTime, "Screen Time", "#9B59B6", true, true);

  createRiskBarChart("riskLevelBarChart", riskLevels);
  createRiskPieChart("riskLevelPieChart", riskLevels);
  createDistChart("bloodSugarDistChart", bloodSugar, "Blood Sugar Distribution");
}

function createLineChart(id, x, y, label, color, fillArea = false) {
  new Chart(document.getElementById(id), {
    type: "line",
    data: {
      labels: x,
      datasets: [{
        label,
        data: y,
        borderColor: color,
        backgroundColor: fillArea ? color + '55' : 'transparent',
        fill: fillArea,
        tension: 0.4,
        pointRadius: 3,
        borderWidth: 2,
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: true } },
      scales: {
        x: { title: { display: true, text: "Age" } },
        y: { title: { display: true, text: label } }
      }
    }
  });
}

function createBarChart(id, x, y, label, color, horizontal = false) {
  new Chart(document.getElementById(id), {
    type: 'bar',
    data: {
      labels: x,
      datasets: [{
        label,
        data: y,
        backgroundColor: color
      }]
    },
    options: {
      indexAxis: horizontal ? 'y' : 'x',
      responsive: true,
      plugins: { legend: { display: true } },
      scales: {
        x: { title: { display: !horizontal, text: horizontal ? '' : 'X Axis' } },
        y: { title: { display: true, text: horizontal ? 'Values' : 'Y Axis' } }
      }
    }
  });
}

function createRiskBarChart(id, riskLevels) {
  const counts = [0, 0, 0];
  riskLevels.forEach(v => counts[v]++);
  new Chart(document.getElementById(id), {
    type: "bar",
    data: {
      labels: ["Low", "Moderate", "High"],
      datasets: [{
        label: "Risk Levels",
        data: counts,
        backgroundColor: ["#2ECC71", "#F1C40F", "#E74C3C"]
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true }
      }
    }
  });
}

function createRiskPieChart(id, riskLevels) {
  const counts = [0, 0, 0];
  riskLevels.forEach(v => counts[v]++);
  new Chart(document.getElementById(id), {
    type: "pie",
    data: {
      labels: ["Low", "Moderate", "High"],
      datasets: [{
        data: counts,
        backgroundColor: ["#ABEBC6", "#F9E79F", "#F5B7B1"]
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom' },
        tooltip: { enabled: true }
      }
    }
  });
}

function createDistChart(id, data, label) {
  const bins = { "60-89": 0, "90-119": 0, "120-149": 0, "150-179": 0, "180+": 0 };
  data.forEach(v => {
    if (v < 90) bins["60-89"]++;
    else if (v < 120) bins["90-119"]++;
    else if (v < 150) bins["120-149"]++;
    else if (v < 180) bins["150-179"]++;
    else bins["180+"]++;
  });

  new Chart(document.getElementById(id), {
    type: "bar",
    data: {
      labels: Object.keys(bins),
      datasets: [{
        label,
        data: Object.values(bins),
        backgroundColor: "#5DADE2"
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: true } },
      scales: {
        y: { beginAtZero: true }
      }
    }
  });
}

document.addEventListener("DOMContentLoaded", loadData);
