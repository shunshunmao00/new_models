import './vendor.ts';

import { NgModule, Injector } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { Ng2Webstorage } from 'ngx-webstorage';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MAT_DIALOG_DEFAULT_OPTIONS } from '@angular/material';
import { MaterialModule } from './material.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AppSharedModule } from './shared';
import { AppMainRoutingModule} from './app-routing.module';
import { MainComponent } from './main/main.component';
import { AppHomeModule } from './home';

@NgModule({
    imports: [
        FormsModule,
        ReactiveFormsModule,
        BrowserModule,
        BrowserAnimationsModule,
        MaterialModule,
        AppMainRoutingModule,
        Ng2Webstorage.forRoot({ prefix: 'my', separator: '-'}),
        AppSharedModule,
        AppHomeModule,
    ],
    declarations: [
        MainComponent,
    ],
    providers: [
        {
            provide: MAT_DIALOG_DEFAULT_OPTIONS,
            useValue: {
                hasBackdrop: true,
                disableClose: true,
            }
        }
    ],
    bootstrap: [ MainComponent ]
})
export class AppMainModule {}
