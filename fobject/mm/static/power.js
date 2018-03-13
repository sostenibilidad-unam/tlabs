var ego_ids = document.currentScript.getAttribute('ego_ids');

$.getJSON("/power_json/", function (data) {
    var cy = cytoscape({
	container: document.getElementById('cy'),
	elements: data,

	style: cytoscape.stylesheet()
	    .selector('node')
	    .css({
		'shape': 'data(shape)',
		'width': 'data(width)',
		'height': 'data(height)',
		'border-width': 2,
		'border-opacity': 0.666,
		'border-color': 'grey',
		'content': 'data(id)',
		'text-valign': 'center',
		'font-size': '1em',
		"text-wrap": "wrap",
		"text-max-width": 80,
		'background-color': '#fef',
		'font-family': 'serif',
		'color': 'black',
		'background-image': 'data(avatar)',
		'background-fit': 'cover'
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
