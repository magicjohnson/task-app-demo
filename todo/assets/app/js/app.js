var app = angular.module(
    'app', ['ngResource', 'ngCookies', 'app.controllers', 'app.services']
);

app.run(function ($http, $cookies) {
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.xsrfCookieName = 'csrftoken';
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.config(function ($resourceProvider) {
    $resourceProvider.defaults.stripTrailingSlashes = false;

});
