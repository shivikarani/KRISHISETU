
fetch('/api/market-prices/')
.then(response => response.json())
.then(data => {

    let table = document.getElementById("mandi-data");

    data.forEach(item => {
        let row = `<tr>
            <td>${item.crop}</td>
            <td>${item.mandi}</td>
            <td>${item.state}</td>
            <td>${item.min_price}</td>
            <td>${item.max_price}</td>
            <td>${item.modal_price}</td>
        </tr>`;

        table.innerHTML += row;
    });

});
