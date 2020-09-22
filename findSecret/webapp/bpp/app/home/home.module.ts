import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { MaterialModule} from '../material.module';
import { AppSharedModule } from '../shared';
import { FileUploadModule } from 'ng2-file-upload';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {CommonModule} from '@angular/common';
import { PopoverModule, BsDropdownModule } from 'ngx-bootstrap';
import {VisModule} from 'ng2-vis';
import {ColorPickerModule} from 'ngx-color-picker';

import {
    HomeComponent,
    PageHeaderComponent,
} from './';

@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        ReactiveFormsModule,
        VisModule,
        ColorPickerModule,
        MaterialModule,
        AppSharedModule,
        FileUploadModule,
        BsDropdownModule.forRoot(),
        PopoverModule.forRoot(),
    ],
    declarations: [
        HomeComponent,
        PageHeaderComponent,
    ],
    entryComponents: [
    ],
    providers: [
    ],
    schemas: [CUSTOM_ELEMENTS_SCHEMA]

})
export class AppHomeModule {}
