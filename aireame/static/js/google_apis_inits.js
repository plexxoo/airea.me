/*
* Este fichero forma parte de airea.me
*
* Copyright 2011 PLEXXOO INTERACTIVA S.L.
* Copyright Daniel Gonzalez     <demetrio@plexxoo.com>
* Copyright Silvia Martín       <smartin@plexxoo.com>
* Copyright Jon Latorre         <moebius@plexxoo.com>
* Copyright Jesus Martinez      <jamarcer@plexxoo.com>
*
* Este fichero se distribuye bajo la licencia GPL según las
* condiciones que figuran en el fichero 'licence' que se acompaña.
* Si se distribuyera este fichero individualmente, DEBE incluirse aquí
* las condiciones expresadas allí.
*
* 
* This program is free software; you can redistribute it and/or
* modify it under the terms of the GNU General Public License
* as published by the Free Software Foundation; either version 2
* of the License, or (at your option) any later version.
* 
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
* 
* You should have received a copy of the GNU General Public License
* along with this program; if not, write to the Free Software
* Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
*/


/** Funciones para arrancar los apis de google **/
var AireaMeGoogleApis = {
	url_base: "http://192.168.1.36:8000/protoaireame",
	url_location: "/api/last.json/LLOD1",
	default_width: 800,
	
	/* Map */
	initializeMap: function(lat, lng){
		var latlng = new google.maps.LatLng(lat, lng);
		var myOptions = {
			zoom: 8,
			center: latlng,
			mapTypeId: google.maps.MapTypeId.ROADMAP
	    };
	    var map = new google.maps.Map(document.getElementById("map_canvas"),myOptions);
	},
	
	
	/* Motion Chart*/
	getDataMotionChart: function() {
		$.ajax({
	    	url: url_base+"/api/statistics.json/LLOD1",
			dataType: 'json',
			success: AireaMeGoogleApis.drawMotionChart
		});
	},
			
	drawMotionChart:function (json_data) {
		var items=[]; 
		$.each(json_data, function(key, val) {
			items.push([val.name, new Date(val.date) , val.value, val.element]);
		});
		var data = new google.visualization.DataTable();
		data.addColumn('string', 'Name');
		data.addColumn('date', 'Date');
		data.addColumn('number', 'Value');
		data.addColumn('string', 'Element');
		data.addRows(items);
		var chart = new google.visualization.MotionChart(document.getElementById('chart_div'));
		chart.draw(data, {width: 600, height:300});
	},


	/* line chart */
	
	getMobileDataLinearChart: function(){
		//google.setOnLoadCallback(AireaMeGoogleApis.getDataLinearChart);
		AireaMeGoogleApis.isMobile = true;
		AireaMeGoogleApis.getDataLinearChart();
	},

	getDataLinearChart: function () {
		$.ajax({
	    	url: AireaMeGoogleApis.url_base + AireaMeGoogleApis.url_location,
			dataType: 'json',
			success: AireaMeGoogleApis.drawLinearChart
		});
	},
			

	drawLinearChart: function (json_data) {
		var data = new google.visualization.DataTable();
		data.addColumn('string', 'Name');
		$.each(json_data['columns'], function(key,val) {
			data.addColumn('number', val);
		});
	 
		var items=[]; 
		$.each(json_data['values'], function(key, val) {
			var ident = [key.toString()];
			var data = ident.concat(val);
			items.push(data);
		});
		data.addRows(items);
		if (AireaMeGoogleApis.isMobile) {
			width = $(document).width();
		} else {
			width = AireaMeGoogleApis.default_width;
		}
		// Create and draw the visualization.
		new google.visualization.LineChart(document.getElementById('chart_div')).
			draw(data, {curveType: "function",
						width: width, height: 400,
						vAxis: {maxValue: 10}}
		);
	},
	
};





/* Motion chart */
		

