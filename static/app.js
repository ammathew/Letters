aa = angular.module('myServiceModule', ['ui.bootstrap']);
aa.config(['$interpolateProvider', function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
  }]);

aa.controller('DashboardCtrl', ['$scope', 'searchTwitterFactory', function ($scope, searchTwitterFactory, $http ) {
    $scope.searchTwitter = function( companyName ) {
	console.log( $scope.companyName )
	$scope.start = '';
	$scope.end = '';
	searchTwitterFactory( companyName, $scope.start, $scope.end ).success( function( data){
	    $scope.timeAndSent = data;
	})
    }
    }]);
  
aa.factory('searchTwitterFactory', function($http) {
    return function( companyName, start, end ) {
	console.log( start );
	return $http({
	    method: 'GET',
            url: '/api/company-info',
	    params : { 
		search_term : companyName,
		start_time : start,
		end_time : end
	    }
	});
    }
});

aa.directive( 'sentchart', function() {
    return {
	restrict: 'E',
	link: function( scope, elem, attr ) {
	    scope.$watch( 'timeAndSent', function(newValue, attr) {
		console.log( 'yo!' );
		console.log( elem );
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