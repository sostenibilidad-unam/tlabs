var ego_ids = document.currentScript.getAttribute('ego_ids');

$.getJSON("/power_json/", function (data) {
    console.log(data);
    var cy = cytoscape({
	container: document.getElementById('cy'),
	elements: data,

	style: cytoscape.stylesheet()
	    .selector('node')
	    .css({
		'shape': 'octagon',
		'width': 60,
		'height': 60,
		'border-width': 2,
		'border-opacity': 0.666,
		'border-color': 'grey',
		'content': 'data(id)',
		'text-valign': 'center',
		'font-size': '1em',
		"text-wrap": "wrap",
		"text-max-width": 60,
		'background-color': '#fef',
		'font-family': 'serif',
		'color': 'black',

	    })
	    .selector(':selected')
	    .css({
		'border-width': 3,
		'border-color': '#333'
	    })
	    .selector('edge')
	    .css({
		'curve-style': 'bezier',
		'opacity': 0.666,
		'line-color': 'green',
		'width': 10
	    }),

	layout: {
	    name: 'cose',
	    fit: true,
	    padding: 100
	}
    });

});
