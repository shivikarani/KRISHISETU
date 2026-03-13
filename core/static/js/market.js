


fetch("/api/market-prices/")
.then(response => response.json())
.then(data => {

    const tableBody = document.querySelector("#marketTable tbody");
    tableBody.innerHTML = "";

    data.forEach(item => {

        const row = `
        <tr>
            <td>${item.commodity}</td>
            <td>${item.market}</td>
            <td>${item.state}</td>
            <td>${item.min_price}</td>
            <td>${item.max_price}</td>
            <td>${item.modal_price}</td>
        </tr>
        `;

        tableBody.innerHTML += row;

    });

});

function searchCrop(){

    const input = document.getElementById("cropSearch").value.toLowerCase()
    const rows = document.querySelectorAll("#marketTable tbody tr")

    rows.forEach(row => {

        const crop = row.cells[0].innerText.toLowerCase()

        if(crop.includes(input)){
            row.style.display = ""
        }else{
            row.style.display = "none"
        }

    })

}


function filterData() {

    const cropInput = document.getElementById("cropSearch").value.toLowerCase()
    const stateInput = document.getElementById("stateFilter").value

    const rows = document.querySelectorAll("#marketTable tbody tr")

    rows.forEach(row => {

        const crop = row.cells[0].innerText.toLowerCase()
        const state = row.cells[2].innerText

        const cropMatch = crop.includes(cropInput)
        const stateMatch = (stateInput === "" || state === stateInput)

        if (cropMatch && stateMatch) {
            row.style.display = ""
        } else {
            row.style.display = "none"
        }

    })
}