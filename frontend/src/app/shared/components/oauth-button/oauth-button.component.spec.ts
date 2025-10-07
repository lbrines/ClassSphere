import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OAuthButtonComponent } from './oauth-button.component';

describe('OAuthButtonComponent', () => {
  let fixture: ComponentFixture<OAuthButtonComponent>;
  let component: OAuthButtonComponent;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [OAuthButtonComponent],
    });

    fixture = TestBed.createComponent(OAuthButtonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should emit click event when button pressed', () => {
    spyOn(component.clicked, 'emit');
    const button: HTMLButtonElement = fixture.nativeElement.querySelector('button');
    button.click();
    expect(component.clicked.emit).toHaveBeenCalled();
  });
});
