var ipScannerControllers = angular.module('ipScannerControllers', []);
ipScannerControllers.controller('ipScannerCtrl', ['$scope', 'IPs', '$interval', function($scope, IPs, $interval){
   $scope.test = "blah!!!!!!!!";
   $scope.ips = IPs.query();
   $scope.loadData = function () {
      $scope.ips = IPs.query();
   }
   $scope.toint = function(num) {
      return parseInt(num);
   }
   $scope.refreshTime = 10;
   $scope.refreshPromise = $interval($scope.loadData(), $scope.refreshTime * 60 * 1000);
   $scope.updateRefresh = function () {
      $interval.cancel($scope.refreshPromise);
      $interval($scope.loadData(), $scope.refreshTime * 60 * 1000);
   }
   
   $scope.subnets = {};
   $scope.toggledns = true;
   $scope.selectall = function (state) {
      angular.forEach($scope.subnets, function(value, key) {
         this[key] = state;
      }, $scope.subnets);   
   }
   $scope.selectvar = "None";
   $scope.selecttoggle = function() {
      if ($scope.selectvar === "All") {
         $scope.selectall(true);
         $scope.selectvar = "None";
      } else {
         $scope.selectall(false);
         $scope.selectvar = "All";
      }
   }
}]);
