document.addEventListener("DOMContentLoaded", function () {
  fetch("/history")
    .then((response) => response.json())
    .then((data) => displayHistory(data))
    .catch((error) => console.error("Error fetching history:", error));
});

function displayHistory(data) {
  const tableBody = document.querySelector("#historyTable tbody");

  // Clear any existing rows
  tableBody.innerHTML = "";

  if (data.length === 0) {
    const noDataRow = document.createElement("tr");
    const noDataCell = document.createElement("td");
    noDataCell.colSpan = 4;
    noDataCell.textContent = "No history records found.";
    noDataCell.style.textAlign = "center";
    noDataCell.style.padding = "16px";
    noDataRow.appendChild(noDataCell);
    tableBody.appendChild(noDataRow);
    return;
  }

  // Populate table rows
  data.forEach((item, index) => {
    const row = document.createElement("tr");

    const idCell = document.createElement("td");
    idCell.textContent = item.id || index + 1;

    const nameCell = document.createElement("td");
    nameCell.textContent = item.name || "N/A";

    const dateCell = document.createElement("td");
    const formattedDate = new Date(item.date).toLocaleString();
    dateCell.textContent = formattedDate || "N/A";

    const resultCell = document.createElement("td");
    resultCell.textContent = item.result || "N/A";

    row.appendChild(idCell);
    row.appendChild(nameCell);
    row.appendChild(dateCell);
    row.appendChild(resultCell);

    tableBody.appendChild(row);
  });
}
