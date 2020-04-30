    var map, heatmap

    var yellow = [
    'rgba(255, 255, 0, 0)',
    'rgba(255, 255, 0, 1)'
    ];

    var red = [
    'rgba(255, 0, 0, 0)',
    'rgba(255, 0, 0, 1)'
    ];

    var green = [
    'rgba(0, 255, 0, 0)',
    'rgba(0, 255, 0, 1)'
    ];

     var firebaseConfig = {
      apiKey: "AIzaSyDwK2f_i2mT8bZR3Gqps8m0o1xHhxyM0Lk",
      authDomain: "wedapp-266618.firebaseapp.com",
      databaseURL: "https://wedapp-266618.firebaseio.com",
      projectId: "wedapp-266618",
      storageBucket: "wedapp-266618.appspot.com",
      messagingSenderId: "96073401336",
      appId: "1:96073401336:web:b1d615bae9ad5116f7cc0d"
    };

    firebase.initializeApp(firebaseConfig);

    var dbRef = firebase.database().ref('wedapp-266618');

    function initMap() {
      map = new google.maps.Map(document.getElementById('map'), {
        zoom: 13,
        center: {lat: 31.5204, lng: 74.3587},
        mapTypeId: 'satellite',
        mapTypeControl: false
      });
	  map.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(document.getElementById('legend'));
	  
      var result,lat,longi,heatmapData,pointArray ;
      dbRef.on('value', function(snapshot) {
        snapshot.forEach(function(child) {
          var childs=child.val();
          result = childs.result;
          lat = childs.latitude;
          longi = childs.longitude;
          heatmapData = [new google.maps.LatLng(lat, longi)];
          pointArray = new google.maps.MVCArray(heatmapData);
          console.log(childs.result);
          heatmap = new google.maps.visualization.HeatmapLayer({
            data:pointArray,
            map: map,
            radius: 24
          });
          if (result == 0 )
            heatmap.set('gradient', heatmap.get('gradient') ? null : yellow);
          if (result == 1)
            heatmap.set('gradient', heatmap.get('gradient') ? null : red);
          if (result == 2)
              heatmap.set('gradient', heatmap.get('gradient') ? null : green);
          });
      });
    }