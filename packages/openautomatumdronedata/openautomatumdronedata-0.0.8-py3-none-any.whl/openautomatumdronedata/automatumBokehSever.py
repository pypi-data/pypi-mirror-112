from bokeh.server.server import Server
from bokeh.layouts import column, row
from bokeh.models import *
from bokeh.plotting import Figure
from openautomatumdronedata.dataset import droneDataset
from bokeh.palettes import Dark2_5 as palette
import os
import itertools  
import math
import copy

def generate_lines_to_plot_object(x, y, psi, l = 5, w = 2):
    """
        This Functions generates a list of x and y coordinates 
        thats plot a vehicle with on the given position, with the 
        heading psi and the length and width.
    """
    x_vr = math.cos(psi) * l/2 - math.sin(psi) * -w/2 + x

    x_vl = math.cos(psi) * l/2 - math.sin(psi) * w/2 + x

    x_hr = math.cos(psi) * -l/2 - math.sin(psi) * -w/2 + x

    x_hl = math.cos(psi) * -l/2 - math.sin(psi) * w/2 + x

    y_vr = math.sin(psi) * l/2 + math.cos(psi) * -w/2 + y

    y_vl = math.sin(psi) * l/2 + math.cos(psi) * w/2 + y

    y_hr = math.sin(psi) * -l/2 + math.cos(psi) * -w/2 + y

    y_hl = math.sin(psi) * -l/2 + math.cos(psi) * w/2 + y

    x_vec = [x_vr, x_vl, x_hl, x_hr, x_vr, x, x_vl]
    y_vec = [y_vr, y_vl, y_hl, y_hr, y_vr, y, y_vl]

    return(x_vec, y_vec)


class automatumDataBokeh():
    """
        Main Class for the automatum bokeh server
    """

    def __init__(self, curDoc):
        self.curDoc = curDoc
        self._reset_internal_states()

        self.curDoc.add_root(self.load_bokeh_objects())

    def _reset_internal_states(self):
        """
            Resets all internal states, so that all values 
            could be easily reset if a new dataset is loaded.
        """
        self.live_plot_time = 0
        self.dataset = None
        self.live_video_play = False
        self.static_world_line_dict = None        
    #
    #
    # Rendering
    #
    #
    def create_static_world_line_dict(self):
        """
            Creates the multi line data dict for rendering the static world. 
            To ensure fast rendering 
        """
        self.static_world_line_dict = {
            "xdata": [],
            "ydata": [],
            "color": [],            
        }

        static_line_list = self.dataset.statWorld.get_lane_marking_dicts()
        for lane_markings in static_line_list:
            self.static_world_line_dict["xdata"].append(lane_markings["x_vec"])
            self.static_world_line_dict["ydata"].append(lane_markings["y_vec"])
            if(lane_markings["type"] == "broken"):
                self.static_world_line_dict["color"].append("grey")
            else:
                self.static_world_line_dict["color"].append("black")


    def render_live_plot(self, time):
        """
            This functions renders the live plot for a given time.
        """
        if(self.dataset is None):
            print("Please load a dateset.")
            return 


        if(self.static_world_line_dict is None):
            self.create_static_world_line_dict()
        live_plot_dict = copy.deepcopy(self.static_world_line_dict)

        colors = itertools.cycle(palette)
        
        objList = self.dataset.dynWorld.get_list_of_dynamic_objects_for_specific_time(time)
        for color, obj in zip(colors, objList):
            idx = obj.next_index_of_specific_time(time)
            (x_vec, y_vec) = generate_lines_to_plot_object(obj.x_vec[idx], obj.y_vec[idx], obj.psi_vec[idx], l = obj.length, w = obj.width)
            live_plot_dict["xdata"].append(x_vec)
            live_plot_dict["ydata"].append(y_vec)
            live_plot_dict["color"].append(color)

        self.live_plot_data.data = live_plot_dict

        self.livePlotTitle.text = 'Live plot of dataset (t = %.2f/%.2f):'%(time, self.dataset.dynWorld.get_length_of_dataset_in_seconds())


    #
    #
    # Rendering
    #
    #

    def render_trajectories(self):
        """
            This functions renders the trajectories plot. 
        """
        obj_list = self.dataset.dynWorld.get_list_of_dynamic_objects()
        colors = itertools.cycle(palette)
        if(self.static_world_line_dict is None):
            self.create_static_world_line_dict()


        data_dict = copy.deepcopy(self.static_world_line_dict )
        for color, obj in zip(colors, obj_list):
            data_dict["xdata"].append(obj.x_vec)
            data_dict["ydata"].append(obj.y_vec)
            data_dict["color"].append(color)

        self.traj_plot_data.data = data_dict
    #
    #
    # Callbacks
    #
    #
    def load_new_dataset(self):
        """
            Callback for load Button. 
            Start loading a new dataset.
        """
        path2Dataset = self.data_set_path_input.value
        self._reset_internal_states()
        if(not os.path.isdir(path2Dataset)):
            print("Please give a path to a valid dataset folder. The given input %s could not be found"%(path2Dataset))
            return 
        self.dataset = droneDataset(path2Dataset)
        self.render_trajectories()
        self.render_live_plot(0)
        self.curDoc.add_periodic_callback(self.periodic_call_back, self.dataset.dynWorld.delta_t*1000)

    def play_video(self):
        """
            Callback play button. 
            Sets the internal flag to start with playing the live plot.
        """
        if(self.dataset is None):
            print("Please load a dateset before pressing play.")
            return         
        self.live_video_play = True
        

    def pause_video(self):
        """
            Callback pause button. 
            Resets the internal flag to start with playing the live plot.
        """        
        self.live_video_play = False

    def go_video(self):
        """
            Callback for go-to-time function. 
            Checks the given value in the text field and show it. 
        """
        user_string = self.animation_time_text_field.value
        try:
            user_time = float(user_string)
        except:
            print("Can't convert your string into a valid time stamp. Please give in format like 1.03.")
            return
        if(user_time >= self.dataset.dynWorld.get_length_of_dataset_in_seconds()):
            print("The given time is large as the dataset!")
            return 
        if(user_time < 0):
            print("The give time is negative.")
            return
        self.live_plot_time = user_time
        self.render_live_plot(self.live_plot_time)

    def step_forward(self):
        """
            Callback for step-forward method. 
            Additionally internal function thats is called for enable live plotting.
        """
        if(self.dataset is None):
            print("Please load a dateset.")
            return    
        animation_speed_factor = self.play_speed_slider.value  
        self.live_plot_time += self.dataset.dynWorld.delta_t * animation_speed_factor
        if(self.live_plot_time >= self.dataset.dynWorld.get_length_of_dataset_in_seconds()):
            self.live_plot_time = 0
        self.render_live_plot(self.live_plot_time)

    def step_backward(self):
        """
            Callback for step_backward button.
        """
        if(self.dataset is None):
            print("Please load a dateset.")
            return 
        if(self.live_video_play):
            print("Stepping is only possible when live play is paused.")                      
        self.live_plot_time -= self.dataset.dynWorld.delta_t
        if(self.live_plot_time < 0):
            self.live_plot_time = self.dataset.dynWorld.get_length_of_dataset_in_seconds()
        self.render_live_plot(self.live_plot_time)

    def periodic_call_back(self):
        """
            Periodic Callback to enable live plotting. 
        """
        if(self.live_video_play is True):
            self.step_forward()



    #
    #
    # Layout 
    #
    #

    def create_live_plot(self):
        """
            Creates the layout for the live plotting area. 
        """
        # Add Figures
        self.livePlotTitle = Title()
        self.livePlotTitle.text = 'Live plot of dataset:'
        self.live_plot = Figure(plot_width=1000, plot_height=1000, match_aspect=True)
        self.live_plot.title = self.livePlotTitle
        self.live_plot_data = ColumnDataSource(data={
            "xdata": [],
            "ydata": [],
            "color": [],

        })
        self.live_plot.multi_line(xs='xdata', ys='ydata', source=self.live_plot_data, line_color='color')

        self.start_button =  Button(label="Play", max_width = 150)
        self.start_button.on_click(self.play_video)
        self.pause_button =  Button(label="Pause", max_width = 150)
        self.pause_button.on_click(self.pause_video)            

        self.step_backwards_button =  Button(label="<<", max_width = 40)
        self.step_backwards_button.on_click(self.step_backward) 
        self.step_forwards_button =  Button(label=">>", max_width = 40)
        self.step_forwards_button.on_click(self.step_forward) 

        self.play_speed_slider = Slider(start=1, end=5, value=1, step=1, title="Select speed of animation", max_width = 200)

        self.animation_time_text_field = TextInput(value="0.0", title="Jump to time:", max_width = 200)
        self.go_button =  Button(label="Go", max_width = 200)
        self.go_button.on_click(self.go_video)           

        
        return row(column(self.start_button, 
                        self.pause_button, 
                        row(self.step_backwards_button, self.step_forwards_button), 
                        self.play_speed_slider,
                        self.animation_time_text_field, 
                        self.go_button,
                         max_width = 250, min_width = 250 ), self.live_plot)


    def create_traj_plot_elements(self):
        """
            Creates the layout for the trajectory plotting area. 
        """        
        # Add Figures
        t = Title()
        t.text = 'Trajectories of dataset:'
        self.traj_plot = Figure(plot_width=1000, plot_height=1000, match_aspect=True)
        self.traj_plot.title = t
        self.traj_plot_data = ColumnDataSource(data={
            "xdata": [],
            "ydata": [],
            "color": [],
        })

        self.traj_plot.multi_line(xs='xdata', ys='ydata', source=self.traj_plot_data, line_color='color')


        return row(column(max_width = 250, min_width = 250),self.traj_plot)

    def create_data_set_choice(self):
        """
            Creates the layout for the data choice area
        """
        self.data_set_path_input = TextInput(title="Give path to dataset folder:", min_width = 1000)

        self.load_dataset_button =  Button(label="Load Dataset", max_width = 150)
        self.load_dataset_button.on_click(self.load_new_dataset)        
        return column(self.data_set_path_input, self.load_dataset_button)

    def load_bokeh_objects(self):
        """
            Function to creates the main bokeh layout
        """
        return column(
            Div(text='<h1 style="text-align: center"> Automatum-Data Dronedata Visualization </h1>'),
            self.create_data_set_choice(),
            self.create_traj_plot_elements(),
            self.create_live_plot()
        )

def main():
    print('Opening Bokeh application on http://localhost:5000/')

    # Setting num_procs here means we can't touch the IOLoop before now, we must
    # let Server handle that. If you need to explicitly handle IOLoops then you
    # will need to use the lower level BaseServer class.

    server = Server({'/': automatumDataBokeh}, num_procs=1)
    server.start()
    server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()

if __name__ == "__main__":
    main()