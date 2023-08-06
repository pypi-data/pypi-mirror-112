var app = angular.module("avocadoPrediction", ['ngMaterial', 'ngMessages']);

app.config(function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.controller("avocadoPredictionCtrl", function ($scope, $http) {
    $scope.init = function () {
        $http.get('/default/')
            .then(
                function (response) {
                    $scope.avocado = response;
                });
        $scope.predicted_average_price = undefined;
        $scope.error = undefined;
    };
    $scope.init();

    $scope.predict = function () {
        $http.post('/predict/', $scope.avocado)
            .then(
                function (response) {
                    $scope.error = undefined;
                    $scope.predicted_average_price = response.data.predicted_average_price;
                },
                function (error) {
                    $scope.predicted_average_price = undefined;
                    $scope.error = error.statusText;
                });
    }
});

app.directive('numberInput', function () {
    return {
        restrict: 'E',
        template: function (elem, attr) {
            return `<md-input-container flex="${attr.flex}">
                        <label>${attr.label}</label>
                        <input type="number" ng-model="avocado.${attr.name}" aria-label="${attr.label}" required min="0" >
                        <div ng-messages="predictForm.${attr.name}.$error" multiple md-auto-hide="false">
                            <div ng-message="required">Number of ${attr.label} is required.</div>
                            <div ng-message="min">Number of ${attr.label} must be natural.</div>
                        </div>
                    </md-input-container>`
        }
    };
});