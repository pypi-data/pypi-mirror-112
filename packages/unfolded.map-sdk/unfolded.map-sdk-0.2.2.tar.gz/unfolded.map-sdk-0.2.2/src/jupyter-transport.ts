import { UnfoldedMapModel } from './widget-model';
import { UnfoldedMap } from '@unfolded/map-sdk';

export interface Message {
  messageId: string;
  type: string;
  data: object;
}

/**
 * These must match to the fields of the Python class models.MapEventHandlers
 */
enum CallbackNames {
  ON_LOAD = 'on_load',
  ON_FILTER = 'on_filter',
  ON_TIMELINE_INTERVAL_CHANGE = 'on_timeline_interval_change',
  ON_LAYER_TIMELINE_TIME_CHANGE = 'on_layer_timeline_time_change',
  ON_HOVER = 'on_hover',
  ON_CLICK = 'on_click'
}

export default class JupyterTransport {
  private readonly model: UnfoldedMapModel;
  private readonly queue: Array<Message> = new Array<Message>();
  private mapReady: boolean = false;
  private destroyed: boolean = false;

  constructor(model: UnfoldedMapModel) {
    this.model = model;
    this.model.on('msg:custom', this.messageReceived);
    this.model.listenTo(this.model, 'destroy', this.finalize);
  }

  setMapReady(value: boolean) {
    this.mapReady = value;
    if (this.mapReady) {
      let msg;
      while ((msg = this.queue.shift()) !== undefined) {
        this.sendMessageToMapSDK(msg);
      }
      const map: UnfoldedMap = this.model.get('map');
      if (map) {
        // Register all callbacks
        map.setMapEventHandlers({
          onFilter: info =>
            this.sendCallbackEventToJupyter(CallbackNames.ON_FILTER, info),
          onLoad: () => this.sendCallbackEventToJupyter(CallbackNames.ON_LOAD),
          onTimelineIntervalChange: info =>
            this.sendCallbackEventToJupyter(
              CallbackNames.ON_TIMELINE_INTERVAL_CHANGE,
              info
            ),
          onLayerTimelineTimeChange: info =>
            this.sendCallbackEventToJupyter(
              CallbackNames.ON_LAYER_TIMELINE_TIME_CHANGE,
              info
            ),
          onHover: info =>
            this.sendCallbackEventToJupyter(
              CallbackNames.ON_HOVER,
              info
            ),
          onClick: info =>
            this.sendCallbackEventToJupyter(
              CallbackNames.ON_CLICK,
              info
            )
        });
      }
    }
  }

  protected finalize = () => {
    this.destroyed = true;
    this.model.off('msg:custom', this.messageReceived);
    this.model.stopListening(this.model, 'destroy', this.finalize);
    const map: UnfoldedMap = this.model.get('map');
    if (map) {
      // Unregister all callbacks
      map.setMapEventHandlers(null);
    }
  };

  /**
   * Forwards messages received from Jupyter to Map SDK
   * @param message
   * @param buffers
   */
  protected messageReceived = (
    message: Message,
    buffers?: ArrayBuffer[] | ArrayBufferView[]
  ) => {
    if (this.destroyed) return;
    console.log('messageReceived', message);

    if (this.mapReady) {
      this.sendMessageToMapSDK(message);
    } else {
      // Keep messages in the queue for until map is ready
      this.queue.push(message);
    }
  };

  protected sendMessageToMapSDK(message: Message) {
    const { messageId, type, data } = message;
    const map = this.model.get('map');
    map
      .sendMessage(type, data)
      .then((result: object) => this.sendResponseToJupyter(messageId, result));
  }

  /**
   * Back-channel messaging: sending responses from Map SDK to Jupyter
   */
  protected sendResponseToJupyter = (messageId: string, data: object) => {
    if (this.destroyed) return;
    const response = { messageId, data };
    console.log('sendResponse', response);
    this.model.send(response, []);
  };

  /**
   * Notify Jupyter of a callback event
   */
  protected sendCallbackEventToJupyter = (
    eventType: CallbackNames,
    info: any = undefined
  ) => {
    this.model.send({ eventType, data: info }, []);
  };
}
