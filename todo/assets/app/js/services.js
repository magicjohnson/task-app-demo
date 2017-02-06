var services = angular.module('app.services', []);


services.factory('Task', function ($resource) {
    var task = $resource('/api/v1/tasks/:id/', {id: '@id'}, {
        update: {
            method: 'PUT'
        },
        complete: {
            method: 'POST',
            url: '/api/v1/tasks/:id/complete/'
        }
    });
    task.prototype.isNew = function () {
        return typeof this.id === "undefined";
    };
    task.prototype.isOwner = function () {
        return this.is_own;
    };
    task.prototype.isCompleted = function () {
        return this.status === 'done'
    };
    task.prototype.canChangeStatus = function () {
        return this.is_own | ! this.isCompleted()
    };
    return task;

});
