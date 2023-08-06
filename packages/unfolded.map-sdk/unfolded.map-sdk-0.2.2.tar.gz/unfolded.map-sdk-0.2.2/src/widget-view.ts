import { DOMWidgetView } from '@jupyter-widgets/base';

import '../css/widget.css';
import { UnfoldedMap } from '@unfolded/map-sdk';
import { UnfoldedMapModel } from './widget-model';

export class UnfoldedMapView extends DOMWidgetView {
  initialize() {
    const width = this.model.get('width');
    const height = this.model.get('height');
    const mapUUID = this.model.get('mapUUID');
    const mapUrl = this.model.get('mapUrl');

    const map = new UnfoldedMap({
      mapUUID,
      mapUrl,
      appendToDocument: false,
      width,
      height,
      embed: true,
      onLoad: (this.model as UnfoldedMapModel).onMapLoaded
    });

    // TODO: do we really need to store map in the widget model?
    this.model.set('map', map);
    this.model.save_changes();

    return map;
  }

  render() {
    this.el.classList.add('unfolded-widget');

    const map = this.model.get('map');

    const { iframe } = map;
    this.el.appendChild(iframe);
  }
}
