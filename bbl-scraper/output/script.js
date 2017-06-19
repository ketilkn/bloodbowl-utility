var findAncestor = function(el, tag) {
	    while ((el = el.parentElement) && el.tagName !== tag);
	    return el;
}
var hasClass = function ( target, className ) {
return new RegExp('(\\s|^)' + className + '(\\s|$)').test(target.className);
}

var sortTable = function(table, col, columnElement) {
    var tb = table.tBodies[0], // use `<tbody>` to ignore `<thead>` and `<tfoot>` rows
        tr = Array.prototype.slice.call(tb.rows, 0), // put rows into array
        i;

    var date_check = /\d{4}-[01]\d-[0-3]\d/;
    var reverse = columnElement.classList.toggle("reverse");
    if(columnElement.classList.contains("sort-ascending")){
	reverse = ! reverse;
    } 

    reverse = -((+reverse) || -1);
    tr = tr.sort(function (a, b) { // sort rows
	var value_a = a.cells[col].textContent.trim();
	var value_b = b.cells[col].textContent.trim();

	if (!date_check.test(value_a) && !isNaN(parseFloat(value_a)) && !isNaN(parseFloat(value_b))){
		//console.log("not isNaN '"+a+"' and '"+b+"'");
		return reverse * (parseFloat(value_a) - parseFloat(value_b))
	}
        return reverse * (a.cells[col].textContent.trim().localeCompare(b.cells[col].textContent.trim()));
    });
    for(i = 0; i < tr.length; ++i) {
	    tb.appendChild(tr[i]); // append each row in order
    }
    var numberColumn = table.querySelectorAll("table tbody tr td.number");
    for(i = 0; i < numberColumn.length; i++) {
	numberColumn[i].innerHTML = i+1;
    }
    columnElement.classList.add("sorted");
}

var setupSortableTable = function() {
	var table = document.querySelectorAll("table");
	for(i=0; i < table.length; i++) {
		var column = table[i].querySelectorAll("thead tr td");
		for(j=0; j < column.length; j++) {
			if( !column[j].classList || column[j].classList.contains("not-sortable")) {
				continue;
			}
			column[j].classList.add("sortable");
			column[j].onclick = function(e){
				var ev = e || window.event;
				var target = e.target || e.srcElement;
				var col = target.parentNode.querySelectorAll("td");
				for(l=0; l < col.length; l++) { 
					col[l].classList.remove("current-sort");
					if ( col[l] == target ) {
						var table = findAncestor(target, "TABLE")
						sortTable(table, l, target);
						target.classList.add("current-sort");
					}
				}
			}
		}
	} 

};

document.addEventListener('DOMContentLoaded', function() {
	setupSortableTable();
}, false);
