var myApp = angular.module('myApp', [], function($interpolateProvider) {
    $interpolateProvider.startSymbol('[#');
    $interpolateProvider.endSymbol('#]');
});

function MyCtrl($scope, $http) {
    $scope.name = 'Superhero';
    $scope.getSeries = function() {
	$http({
        method: 'GET',
        url: 'http://www.shareholderletters.net/api/get-timeseries'
     }).success(function(data){
         $scope.timeSeries = data
    }).error(function(){
    });
    }
}