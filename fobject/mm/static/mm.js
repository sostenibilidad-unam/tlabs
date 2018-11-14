var ego_ids = document.currentScript.getAttribute('ego_ids');

$.getJSON("/mm_json/", function (data) {
    console.log(data);
    var cy = cytoscape({
	container: document.getElementById('cy'),

	boxSelectionEnabled: false,
	autounselectify: true,
	elements: data,


  style: [
    {
      selector: 'node',
      css: {
	'content': 'data(name)',
	'text-valign': 'center',
	'text-halign': 'center'
      }
    },
    {
      selector: '$node > node',
      css: {
	'padding-top': '10px',
	'padding-left': '10px',
	'padding-bottom': '10px',
	'padding-right': '10px',
	'text-valign': 'top',
	'text-halign': 'center',
	'background-color': '#bbb'
      }
    },
    {
      selector: 'edge',
      css: {
	  'target-arrow-shape': 'triangle',
	  'line-color': 'pink'
      }
    },
    {
      selector: ':selected',
      css: {
	'background-color': 'black',
	'line-color': 'black',
	'target-arrow-color': 'black',
	'source-arrow-color': 'black'
      }
    }
  ],


	layout: {
	    name: 'circle',
	    animate: true,
	    padding: 100
	}
    });

});
