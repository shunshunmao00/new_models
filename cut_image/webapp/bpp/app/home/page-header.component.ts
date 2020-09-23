import {Component} from '@angular/core';

@Component({
    selector: 'my-pageheader',
    templateUrl: './page-header.component.html',
})
export class PageHeaderComponent  {
    isMobile = window.screen.width < 960;

    gotoDemo() {
        window.location.href = '/popen/#/demo';
    }
}
