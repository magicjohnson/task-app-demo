var controllers = angular.module('app.controllers', []);

controllers.controller('TaskController', function ($scope, Task) {
    $scope.tasks = Task.query();
    $scope.task = new Task();
    $scope.index = -1;

    $scope.editTask = function (task, index) {
        $scope.task = task;
        $scope.index = index;
    };

    $scope.clearForm = function() {
        $scope.task = new Task();
    };

    $scope.addTask = function () {
        $scope.task.$save(function () {
            $scope.tasks.push($scope.task);
        });
    };

    $scope.updateTask = function () {
        $scope.task.$update();
    };

    $scope.deleteTask = function () {
        $scope.task.$delete(function (){
            $scope.tasks.splice($scope.index, 1);
            $scope.clearForm();
        });

    };

    $scope.changeTaskStatus = function (task) {
        if (task.isOwner()) {
            task.$update();
        } else {
            task.$complete();
        }
    };
    $scope.toggleCompleted = function() {
        $scope.hideCompleted = ! $scope.hideCompleted;
    }
});

