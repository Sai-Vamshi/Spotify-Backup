import template from './app.html';
import { AppController as controller } from './app.controller';
import './app.scss';
controller.$inject = ['AppApi','UserAccounts']

export let AppComponent = {
  template,
  controller
}