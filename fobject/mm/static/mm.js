var ego_ids = document.currentScript.getAttribute('ego_ids');

$.getJSON("/mm_json/", function (data) {
    console.log(data);
    var cy = cytoscape({
	container: document.getElementById('cy'),
	elements: data,

	style: cytoscape.stylesheet()
	    .selector('node')
	    .css({
		'shape': 'data(shape)',
		'width': 290,
		'height': 250,
		'border-width': 10,
		'border-opacity': 0.666,
		'border-color': 'grey',
		'content': 'data(id)',
		'text-valign': 'center',
		'font-size': '2em',
		"text-wrap": "wrap",
		"text-max-width": 280,
		'background-color': '#eff',
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
		'line-color': 'firebrick',
		'width': 20
	    }),

	layout: {
	    name: 'breadthfirst',
	    nodeDimensionsIncludeLabels: true,
	    fit: true,
	    padding: 100
	}
    });

});
