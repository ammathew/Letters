
aa = angular.module('myServiceModule', ['ui.bootstrap', 'nvd3ChartDirectives', 'ngRoute' ]);
aa.config(['$interpolateProvider', '$routeProvider', '$locationProvider', function ($interpolateProvider, $routeProvider, $locationProvider ) {

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

aa.controller('DashboardCtrl', ['$scope', 'searchTwitterFactory', '$http', '$location', '$rootScope', '$window',function ($scope, searchTwitterFactory, $http, $location, $rootScope, $window ) {

    $scope.getTweetEnts = function ( tweetText ) {
	$scope.getEntities( tweetText ).success( function( data ) {
            $scope.keywords = data;  
        });
    } 

    $scope.getEntities = function ( text ) {
	data = { text: text } 
        return $http({ 
            method: 'POST',
	    headers: {
		"Content-Type": "application/json"
	    },
	   data: data,
	    url:"/api/extractEnts",
        })
    }

    $scope.searchTwitter = function ( searchTerm ) {
	data = { search_term : searchTerm };
        return $http({ 
            method: 'GET',
	    params: data,
	    url:"/api/searchTwitter",
        })
    }

    /*
    $scope.getHighlightedText = function() {
	$('html').mouseup(function (e){
	    var text = "";
	    if (window.getSelection) {
		var blah = window.getSelection();
		console.log( blah );
		$scope.searchText = window.getSelection().toString();
	    } else if (document.selection && document.selection.type != "Control") {
		$scope.searchText = document.selection.createRange().text;
	    }
	});
    }	
*/

    $scope.getHighlightedText = function() {
	$('html').mouseup(function (e){
	    var text = "";
	    if (window.getSelection && window.getSelection().type == "Range" ) {
		$("mark").contents().unwrap();
		$("mark").remove();
		$scope.selectedText = window.getSelection().toString();
		var selection = window.getSelection();
		var range = selection.getRangeAt(0);
		var cssclass = $(selection.anchorNode.parentNode).attr("class");
		var newNode = document.createElement("mark");
		range.surroundContents(newNode);

	    } else if (document.selection && document.selection.type != "Control") {
		$scope.searchText = document.selection.createRange().text;
	    }
	});
    }	

    $scope.$watch( 'selectedText', function( newValue ) {
	$( "mark" ).click( function() {
	    $scope.searchTwitter( newValue ).success( function( data ){
		$scope.tweetsWithSearchTerm = data.statuses;
	    }); 
	})
	
    })
   
    $scope.getHighlightedText();

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

    $scope.$watch( 'posts', function( newValue ) {
	$scope.allPosts = '';

	if( newValue ) {
	    for( i=0; i< $scope.posts.length; i++ ) {
		console.log( $scope.posts );
		$scope.allPosts = $scope.allPosts + '. ' + $scope.posts[i].text;
	    }
	    console.log( 'get entities' );
	    $scope.getEntities( $scope.allPosts ).success( function(data) {
		$scope.entities = data;	
	    });
	}
	console.log( $scope.allPosts );
    })

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
            console.log( data.redirect_url );  
            $window.location.href = data.redirect_url;
        });
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


aa.directive('blah', function() {
    return {
	scope: '=',
        restrict: 'E',  
        templateUrl: "tweet.html"
    };
});

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


aa.run(function($rootScope, $templateCache) {
   $rootScope.$on('$viewContentLoaded', function() {
      $templateCache.removeAll();
   });
});

