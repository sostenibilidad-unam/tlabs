var ego_ids = document.currentScript.getAttribute('ego_ids');

$.getJSON("/ana_json/", function (data) {
    console.log(data);
    var Cy = cytoscape({
	container: document.getElementById('cy'),
	elements: data,

	style: cytoscape.stylesheet()
	    .selector('node')
	    .css({
		'shape': 'data(shape)',
		'width': 'data(width)',
		'height': 'data(height)',
		'content': 'data(name)',
		'text-valign': 'center',
		"text-wrap": "wrap",
		"text-max-width": 280,
		'background-color': 'data(scolor)',
		'color': 'white',
		'text-outline-width': 2.4,
		'text-outline-color': 'grey',
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
		'width': 'mapData(distance, 1, 3, 2, 10)',
		'source-arrow-shape': 'circle',
		'target-arrow-shape': 'triangle',
		'line-color': 'data(polarity)',
		'source-arrow-color': 'data(polarity)',
		'target-arrow-color': 'data(polarity)',
		'source-label': 'data(source_label)',
		'target-label': 'data(target_label)',
	    })
	    .selector('edge.questionable')
	    .css({
		'line-style': 'dotted',
		'target-arrow-shape': 'diamond'
	    })
	    .selector('.faded')
	    .css({
		'opacity': 0.25,
		'text-opacity': 0
	    }),

	layout: {
	    name: 'dagre',
	    rankDir: 'LR',
	    ranker: 'longest-path',
	    nodeDimensionsIncludeLabels: true,
	    rankSep: 500,
	}
    });


    Cy.on('tap', 'node', function(){
	window.location.href = this.data('href');
    });

});
