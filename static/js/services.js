var ipScannerServices = angular.module('ipScannerServices', ['ngResource']);

ipScannerServices.factory('IPs', ['$resource',
   function($resource){
      return $resource('/ip_scan.json', {}, {
         query: {method:'GET', isArray:false}
      });
   }]);
