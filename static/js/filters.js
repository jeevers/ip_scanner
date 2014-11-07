angular.module('ipScannerFilters', []).filter('stateCSS', function() {
   return function(input) {
      if (input === 'ACTIVE'){
         return 'active';
      } else {
         return 'inactive';
      }
   };
});

angular.module('ipScannerFilters').filter('cidrdeformatter', function() {
   return function(input) {
      return input.replace(/\./g,'_').replace(/\//g,'-');
   };
});
