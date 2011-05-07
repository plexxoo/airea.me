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
	url_base: "",
	url_location: "/api/last.json/LLOD1",
	map_url_location: "/api/station.json",
	default_width: 800,
	is_mobile: false,
	
	
	//map variables
	maps_identifier: new Array(),	
	maps_estacion: new Array(),
	maps_direccion: new Array(), 
	maps_link : new Array(),
	maps_latitude : new Array(),
	maps_longitude : new Array(),

	
	/* Map */
	initializeMap: function(){
		$.ajax({
			url: AireaMeGoogleApis.url_base + AireaMeGoogleApis.map_url_location,
			dataType: 'json',
			success: AireaMeGoogleApis.prepareStations
		});

	},
	
	
	prepareStations: function(json_data) {
		$.each(json_data, function(key,val) {
			AireaMeGoogleApis.maps_identifier[key]=val.id;
			AireaMeGoogleApis.maps_estacion[key]=val.name;
			AireaMeGoogleApis.maps_direccion[key]=val.address;
			AireaMeGoogleApis.maps_link[key]=val.external_url;
			AireaMeGoogleApis.maps_latitude[key]=val.lat
			AireaMeGoogleApis.maps_longitude[key]=val.lon
		});
		AireaMeGoogleApis.startMap();
	},
	
	startMap: function(){
		var latlng = new google.maps.LatLng(43, -2.59); //lat,lng de pais vasco
		var myOptions = {
			zoom: 8,
			center: latlng,
			mapTypeId: google.maps.MapTypeId.ROADMAP,
			zoomControlOptions: {
	          style: google.maps.ZoomControlStyle.SMALL,
	          position: google.maps.ControlPosition.LEFT_CENTER
	      	}
	    };
	    var map = new google.maps.Map(document.getElementById("map_canvas"),myOptions);
	    
	    //add markers:
	    $.each(AireaMeGoogleApis.maps_latitude, function(index,value){
	    	if(index > 0){
	    		var marker = new google.maps.Marker({  
	    			  position: new google.maps.LatLng(AireaMeGoogleApis.maps_latitude[index], AireaMeGoogleApis.maps_longitude[index]), 
	    			  map: map  
	    		});
	    	}
	    });
	},
	
	/* Motion Chart*/
	getDataMotionChart: function() {
		$.ajax({
	    	url: AireaMeGoogleApis.url_base + AireaMeGoogleApis.url_location,
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
		AireaMeGoogleApis.is_mobile = true;
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
		if (AireaMeGoogleApis.is_mobile) {
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
		

