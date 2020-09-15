import {Route, Routes} from '@angular/router';
import {HomeComponent} from './home.component';

const homeRoute: Route = {
    path: '',
    component: HomeComponent,
    data: {
        pageTitle: 'CubeAI模型演示',
    },
};

export const homeRoutes: Routes = [
    homeRoute,
];
