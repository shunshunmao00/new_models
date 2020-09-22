import {NgModule, CUSTOM_ELEMENTS_SCHEMA} from '@angular/core';
import {DatePipe} from '@angular/common';
import { MaterialModule} from '../material.module';
import {MatPaginatorIntl} from '@angular/material';

import {
    AppSharedLibsModule,
    AppSharedCommonModule,
    StateStorageService,
    HtmlPipe,
    SnackBarService,
    ConfirmService,
    ModelClient,
    ConfirmDialogComponent,
    MatPaginatorCn,
} from './';

@NgModule({
    imports: [
        MaterialModule,
        AppSharedLibsModule,
        AppSharedCommonModule,
    ],
    declarations: [
        HtmlPipe,
        ConfirmDialogComponent,
    ],
    entryComponents: [
        ConfirmDialogComponent,
    ],
    providers: [
        StateStorageService,
        DatePipe,
        SnackBarService,
        ConfirmService,
        ModelClient,
        {provide: MatPaginatorIntl, useClass: MatPaginatorCn},
    ],
    exports: [
        AppSharedCommonModule,
        DatePipe,
        HtmlPipe,
    ],
    schemas: [CUSTOM_ELEMENTS_SCHEMA]

})
export class AppSharedModule {
}
