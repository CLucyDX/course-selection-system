function filterTable(type) {
    var table = document.getElementById("myTable");
    var rows = table.getElementsByTagName("tr");
    for (var i = 0; i < rows.length; i++) {
        var cells = rows[i].getElementsByTagName("td");
        if (cells.length > 0) {
            var cell = cells[1]; // Type column
            if (cell.innerHTML === type || type === 'C') {
                rows[i].style.display = "";
            } else {
                rows[i].style.display = "none";
            }
        }
    }
}