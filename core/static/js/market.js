async function loadMarketPrices() {

    try {

        const response = await fetch("/api/market-prices/");

        const data = await response.json();

        console.log(data);

        const tableBody = document.querySelector("#marketTable tbody");

        tableBody.innerHTML = "";

        data.forEach(item => {

            const row = `
                <tr>
                    <td>${item.commodity}</td>
                    <td>${item.market}</td>
                    <td>${item.state}</td>
                    <td>₹${item.min_price}</td>
                    <td>₹${item.max_price}</td>
                    <td>₹${item.modal_price}</td>
                </tr>
            `;

            tableBody.innerHTML += row;

        });

    } catch(error) {

        console.log("ERROR:", error);

    }
}

loadMarketPrices();

function filterData() {

    const cropInput =
        document.getElementById("cropSearch")
        .value
        .toLowerCase();

    const stateInput =
        document.getElementById("stateFilter")
        .value
        .toLowerCase();

    const rows =
        document.querySelectorAll("#marketTable tbody tr");

    rows.forEach(row => {

        const crop =
            row.cells[0].innerText.toLowerCase();

        const state =
            row.cells[2].innerText.toLowerCase();

        const cropMatch =
            crop.includes(cropInput);

        const stateMatch =
            stateInput === "" ||
            state.includes(stateInput);

        if(cropMatch && stateMatch){

            row.style.display = "";

        } else {

            row.style.display = "none";

        }

    });

}