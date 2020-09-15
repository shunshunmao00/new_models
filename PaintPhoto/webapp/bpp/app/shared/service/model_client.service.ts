import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class ModelClient {

    constructor(
        private http: HttpClient,
    ) {}

    access(url, method, kwargs): Observable<HttpResponse<any>> {
        const body = {
            method,
            kwargs,
        };
        return this.http.post<any>(url, body, { observe: 'response' });
    }

}
