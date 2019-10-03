import { Injectable } from '@angular/core';
import { AngularFirestore, AngularFirestoreDocument } from '@angular/fire/firestore';
import { Observable } from 'rxjs';

export interface CurrEnv {
  light: number;
  output_ac: number;
  output_lights: number;
  temperature: number;
  timestamp: any;
}
@Injectable({
  providedIn: 'root'
})
export class FireService {

  private current_envDoc: AngularFirestoreDocument<CurrEnv>;

  constructor(db: AngularFirestore) { 
    this.current_envDoc = db.collection("current_env").doc<CurrEnv>("c_env");
  }

  public getCurrentEnv() {
    return this.current_envDoc.valueChanges();
  }
}
