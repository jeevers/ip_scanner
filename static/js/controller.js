var ipScannerControllers = angular.module('ipScannerControllers', []);
ipScannerControllers.controller('ipScannerCtrl', ['$scope', 'IPs', function($scope, IPs){
   $scope.test = "blah!!!!!!!!";
   $scope.ips = IPs.query();
   $scope.toint = function(num) {
      return parseInt(num);
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
