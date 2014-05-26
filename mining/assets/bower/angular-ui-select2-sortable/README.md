ui-select2-sortable   [![Build Status](https://travis-ci.org/Taranys/ui-select2-sortable.png?branch=master)](https://travis-ci.org/Taranys/ui-select2-sortable)
==========
This directive allows you to enhance your select elements with behaviour from the [select2](http://ivaynberg.github.io/select2/) library.

It is a fork from [ui-select2](https://github.com/angular-ui/ui-select2).

I change it to meet my needs :
* Multiple elements
* Sortable with drag&grop
* Use any JS objects as data without any conversion between select2 model and your model

I removed support of <select> to keep only <input type="hidden"> to simplify the directive.

# TODO
- add filtered example
- (add a filter-query to filter automatically ?)

# Requirements

- [AngularJS](http://angularjs.org/)
- [JQuery](http://jquery.com/)
- [JQueryUi](http://jqueryui.com/)
- [Select2](http://ivaynberg.github.io/select2/)

# Example

You can find a runnable example of lib into docs/index.html

## Setup

1. Install **Karma**, **Grunt** and **Bower**
  `$ npm install -g karma grunt-cli bower`
2. Install development dependencies
  `$ npm install`
3. Install components
  `$ bower install`

## Testing

I use [Grunt](http://gruntjs.com/) to check for JavaScript syntax errors and execute all unit tests. To run Grunt, simply execute:

`$ grunt`

This will lint and test the code, then exit. To have Grunt stay open and automatically lint and test your files whenever you make a code change, use:

`$ grunt karma:server watch`

This will start a Karma server in the background and run unit tests in Firefox and PhantomJS whenever the source code or spec file is saved.

# Usage

I use [bower](https://github.com/bower/bower) for dependency management. Install AngularUI Select2 Sortable into your project by running the command

`$ bower install angular-ui-select2-sortable`

If you use a `bower.json` file in your project, you can have Bower save ui-select2-sortable as a dependency by passing the `--save` or `--save-dev` flag with the above command.

This will copy the ui-select2-sortable files into your `bower_components` folder, along with its dependencies. Load the script files in your application:
```html
<link rel="stylesheet" href="bower_components/select2/select2.css">
<script type="text/javascript" src="bower_components/jquery/jquery.js"></script>
<script type="text/javascript" src="bower_components/jquery/jquery-ui.js"></script>
<script type="text/javascript" src="bower_components/select2/select2.js"></script>
<script type="text/javascript" src="bower_components/angular/angular.js"></script>
<script type="text/javascript" src="bower_components/angular-ui-select2/src/select2sortable.js"></script>
```

(Note that `jquery` must be loaded before `angular` so that it doesn't use `jqLite` internally)


Add the select2 module as a dependency to your application module:

```javascript
var myAppModule = angular.module('MyApp', ['ui.select2.sortable']);
```

Apply the directive to your form elements:

```html
<input type="hidden" ui-select2-sortable ng-model="selection"
    allow-clear='true' simple-query="getObjectsData">
```

```javascript
$scope.getObjectsData = function(term, result) {
    result(["one","two","three"]);
};
```

## Working with ng-model

The ui-select2 directive plays nicely with ng-model.

If you add the ng-model directive to same the element as ui-select2 then the picked option is automatically synchronized with the model value.

Into simple-query attribute, you can use a function and return string array or objects array with the callback.

```html
<input type="hidden" ui-select2-sortable ng-model="selection"
    allow-clear='true' simple-query="getObjectsData">
```

```javascript
$scope.getObjectsData = function(term, result) {
    result([
       { id: 1, label: "one", other: "ONE"},
       { id: 2, label: "two", other: "TWO"},
       { id: 3, label: "three", other: "THREE"}
    ]);
};
```

## Filter data by term

By default, results are not filter by term enter by user.
To do it, the simple way is to use angular $filter to customize the filter.

```javascript
// simple search
$scope.simpleQuery = function (term, callback) {
    var values = ['test','abc'];
    callback($filter('filter')(values, term));
};
```

```javascript
//search on a particular object field
$scope.simpleQuery = function (term, callback) {
    var values = [{name:'test'},{name:'abc'}];
    callback($filter('filter')(values, {name: term}, 'name'));
};
```

Since v0.0.2, it is possible to use :

```javascript
// simple search
$scope.simpleData = ['test','abc'];
```

## Sort possible results
To enable text sorting, you have to add 'sort-results' below.

```html
<input type="hidden" ui-select2-sortable ng-model="selection"
    allow-clear='true' simple-query="getObjectsData"
    sort-results="true">
```

## Sortable

To enable sortable drag&drop, you have to add both 'multiple' and 'sortable' attributes as below.

```html
<input type="hidden" ui-select2-sortable ng-model="selection"
    allow-clear='true' simple-query="getObjectsData"
    multiple sortable>
```

```javascript
$scope.getObjectsData = function(term, result) {
    result(["one","two","three"]);
};
```

## Using any object into query

Objects are automatically manage if you have an id field and a text field.
Id field can be any of those :
* _id
* id
* uri
* href
* resource

Text field can be any of those :
* text
* name
* label

If objects didn't match this rules, you have to set a function to define id field and/or text field as below

```javascript
// return id
$scope.complexId = function (item) {
    return item.complex.split('-')[0];
};

//return displayed label
$scope.complexText = function (item) {
    return item.complex.split('-')[1] + " (" + item.color + ")";
};

//data
$scope.complexData = [
    { complex: "1-test", restLink: "https://www.google.fr/?q=pangolin", color: "red" },
    { complex: "2-another", restLink: "https://www.google.fr/?q=echidna", color: "blue" },
    { complex: "3-thing", restLink: "https://www.google.fr/?q=firefox", color: "green" }
];

//function to simple-query attr
$scope.getComplexData = function (term, done) {
    done($scope.complex);
};
```

```html
<input type="hidden" ui-select2-sortable allow-clear='true' multiple sortable
   ng-model="complexSelectionArray" simple-query="getComplexData"
   to-id="complexId" to-text="complexText">
```