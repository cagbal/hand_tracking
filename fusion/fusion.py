
class Fusion(object):
    def __init__(self):
        self.hand_pos_x = 0
        self.hand_pos_y = 0
    
    def fuse(self, object_map, image_width, image_height):
        #TODO: Object out and object id is hard coded for now
        
        event_type = "object-out"

        if self.hand_pos_x > image_width/2:
            position = "left"

            print(image_width, self.hand_pos_x)
            
            probability = (self.hand_pos_x-image_width/2)/image_width
        else:
            position = "right"

            print(image_width, self.hand_pos_x)

            probability = 1-self.hand_pos_x/image_width

        return event_type, position, probability,\
               object_map[position]["object_id"],\
               object_map[position]["object_type"]

    def update_observations(self, hand_tracking_path, scale=0):
        # TODO: Scale should also be implemented
        path = hand_tracking_path[0]
        avg_x, avg_y = 0, 0
        for x, y in path:
            avg_x += x/len(path)
            avg_y += y/len(path)

        self.hand_pos_x = avg_x
        self.hand_pos_y = avg_y