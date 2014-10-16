
console.log( 'yo' );
aa = angular.module('myServiceModule', []);
aa.controller('MyController', ['$scope', 'searchTwitterFactory', 'authTwitterFactory', function ($scope, searchTwitterFactory, authTwitterFactory, $http ) {
//    authTwitterFactory.getDrivers().success( function( data ) {
	console.log( 'afss' );
    });
  

}]);

aa.factory('searchTwitterFactory', function($http) {
    var ergastAPI = {};
    ergastAPI.getDrivers = function() {
      return $http({
	  method: 'jsonp',
        url: 'https://api.twitter.com/1.1/search/tweets.json'
      });
    }

    return ergastAPI;
});


aa.factory('authTwitterFactory', function($http) {
    var ergastAPI = {};
    ergastAPI.getDrivers = function() {
	var aa = '0H68Giqh3XaVPQe0x30IiA:KlV894f9zkuXWdh6pasw9he6PwpcgQYc3XFrLkNJ7t0';
	aa = btoa( aa );
      return $http({
	  method: 'POSTfssd',
          url: 'https://api.twitter.com/oauth2/token',
	  data: { grant_type : 'client_credentials' },
	  headers: { 
	      'Authorizaton': 'Basic ' + aa,
	      'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
	  }
      });
    }

    return ergastAPI;
});
