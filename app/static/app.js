aa = angular.module('myServiceModule', ['ui.bootstrap', 'nvd3ChartDirectives', 'ngRoute' ]);
aa.config(['$interpolateProvider', '$routeProvider', '$locationProvider', function ($interpolateProvider, $routeProvider, $locationProvider ) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');

    $routeProvider
	.when('/register',{
            templateUrl: 'register.html',
            controller: 'AuthCtrl'
        })
	.when('/login',{
            templateUrl: 'login.html',
            controller: 'AuthCtrl'
        })
	.when('/dashboard',{
            templateUrl: 'dashboard.html',
            controller: 'DashboardCtrl'
        }); 

   // $locationProvider.html5Mode( false );
    // was not able to get html5Mode to work. maybe look into History.js .. 
}]);

aa.controller('DashboardCtrl', ['$scope', 'searchTwitterFactory', '$http', '$location', '$rootScope', function ($scope, searchTwitterFactory, $http, $location, $rootScope ) {

    $scope.logOut = function () {
          $http({ 
            method: 'GET',
	    url:"/api/logout",
        }).success( function( data ) {
            $scope.posts = data;
            console.log( data );  
            $location.path( "/" );
        });
    }

    $scope.getPosts = function () {
          $http({ 
            method: 'GET',
	    url:"/api/twitterPosts",
        }).success( function( data ) {
            $scope.posts = data;
            console.log( data );  
        });
    }

    $scope.authTwitter = function() {
        $http({ 
            method: 'GET',
	    url:"/api/authtwitter",
        }).success( function( data ) {
            console.log( data );  
        });
    }

    $scope.radius = 3;
    //$scope.geoData = '';
    $scope.searchTwitter = function( companyName, geoData ) {
	console.log( searchTwitterFactory );
	searchTwitterFactory( companyName, $rootScope.geoData ).success( function( data ){
	    $scope.pieChartData = [];
	    for( var i=0; i<2; i++ ){
		$scope.pieChartData[i] = data[i]
	    }
	    $scope.posts = data[2];
	    
	});
    };

    $scope.$watchCollection( '[ address, radius ]' , function( newValues ) {
	$scope.getGeocode( newValues[0] );	
    });

    $scope.getGeocode = function( address ) {	
        //console.log( 'location' );
        // was not able to get html5mode to work
        //console.log( $location.path() );

	var mapOptions = {
	    address: address
	}
	geocoder = new google.maps.Geocoder();
	geocoder.geocode( mapOptions, function( results ){ 
	    $scope.geocode = results;
	    $rootScope.geoData = $scope.geocode[0].geometry.location.k + "," + $scope.geocode[0].geometry.location.B+ "," + $scope.radius + "mi";
	});
	
    };
    $scope.geocode = {};

    $scope.xFunction = function(){
	return function(d) {
            return d.key;
	}
    };

    $scope.yFunction = function(){
	return function(d) {
	    console.log( d.y );
            return d.y;
	};
    }

}]);
  
aa.factory('searchTwitterFactory', function($http) {
    return function( companyName, geodata ) {
	return $http({
	    method: 'GET',
            url: '/api/company-info',
	    params : { 
		search_term : companyName,
		geocode: geodata
	    }
	});    
    }
});


aa.directive( 'sentchart', function() {
    return {
	restrict: 'E',
	link: function( scope, elem, attr ) {
	    scope.$watch( 'timeAndSent', function(newValue, attr) {
		if ( newValue ) {
		    data = newValue;
		    arr = [];
		    for( i=0; i<data.length; i++ ) {
			obj ={};
			obj['x'] = i;
			obj['y'] = parseInt( data[i].pos * 100 );
			arr.push( obj );
		    }

		    console.log( arr );

		    var graph = new Rickshaw.Graph( {
			element: document.querySelector("#chart"), 
			width: 300, 
			height: 200, 
			series: [{
			    color: 'steelblue',
			    data: arr
			}]
		    });		
		    graph.render();
		}
	    });
	}	
    }
})


aa.controller('AuthCtrl', ['$scope', '$http', '$location',  function ($scope, $http, $location ) {
    
    
    $scope.signup = function(){ 
        var data = {}
        data.username = $scope.username;
        data.password = $scope.password;
        data.email = $scope.email;

        console.log( data );
        
        $http({ 
            method: 'POST',
	    url:"/api/register",
            data: $.param(data),
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        }).success( function( data ) {
            console.log( data );  
        });
    };
    
    
    $scope.login = function() {
        var data = {}
        data.username = $scope.username;
        data.password = $scope.password;

        console.log( data );
        
        $http({ 
            method: 'POST',
	    url:"/api/login",
            data: $.param(data),
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        }).success( function( data ) {
            console.log( data );
            $location.path("/dashboard");
        });
    }


}])

aa.directive( 'reservation', function() {
    return {
	restrict: 'A',
	link: function( scope, elem, attr ) {
	    elem.daterangepicker(null, function(start, end, label) {
                scope.start = start.toISOString();
		scope.end = end.toISOString();
            });
	}	
    }
})
