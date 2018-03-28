function varargout = guiDiffraction(varargin)
% GUIDIFFRACTION MATLAB code for guiDiffraction.fig
%      GUIDIFFRACTION, by itself, creates a new GUIDIFFRACTION or raises the existing
%      singleton*.
%
%      H = GUIDIFFRACTION returns the handle to a new GUIDIFFRACTION or the handle to
%      the existing singleton*.
%
%      GUIDIFFRACTION('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in GUIDIFFRACTION.M with the given input arguments.
%
%      GUIDIFFRACTION('Property','Value',...) creates a new GUIDIFFRACTION or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before guiDiffraction_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to guiDiffraction_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help guiDiffraction

% Last Modified by GUIDE v2.5 20-Mar-2014 09:57:45

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @guiDiffraction_OpeningFcn, ...
                   'gui_OutputFcn',  @guiDiffraction_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before guiDiffraction is made visible.
function guiDiffraction_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to guiDiffraction (see VARARGIN)

% Choose default command line output for guiDiffraction
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);
refreshImages(handles)


% UIWAIT makes guiDiffraction wait for user response (see UIRESUME)
% uiwait(handles.figure1);

function refreshImages(handles)

source=handles.source;
diffraction=handles.diffracted;

hObject= handles.sourceFile;
menuSelection  = get(hObject,'Value');

[x,y]=meshgrid(-10:0.01:10, -10:0.01:10);


f = get(handles.f,'Value');
if f < 1
    f = 1.1;
end

scale = 10^get(handles.scale,'Value');
structureSize = get(handles.size,'Value');;

%image=drawShapeIntoMatrix('square',x,y,structureSize);
    
switch menuSelection
     case 1
        image=generateCenteredSquare(x,y,structureSize);
     case 2
        image=generateCenteredCircle(x,y,structureSize);
     case 3
        image=imread('arbitraire.tif');
     
end
    
complexDiffractionImage = fft2(image);
fieldDiffractionImage=abs(complexDiffractionImage );
normalizedFieldDiffractionImage=fieldDiffractionImage/max(max(fieldDiffractionImage));
normalizedFieldDiffractionImage=fftshift(normalizedFieldDiffractionImage);

[width, height] = size(image);
imshow(image( width*(1/2-1/2/f) : width*(1/2+1/2/f), height*(1/2-1/2/f) : height*(1/2+1/2/f) ),'Parent', source) 
imshow(scale*normalizedFieldDiffractionImage(width*(1/2-1/2/f) : width*(1/2+1/2/f), height*(1/2-1/2/f) : height*(1/2+1/2/f)).^2, 'Parent', diffraction )

function image = drawShapeIntoMatrix(shape, xCoords, yCoords, size)

switch (shape)
    case 'circle'
        image = xCoords.*xCoords + yCoords.*yCoords < size*size;
    case 'square'
        image = abs(xCoords) < size & abs(yCoords) < size;     
end

% --- Outputs from this function are returned to the command line.
function varargout = guiDiffraction_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;

% --- Executes on selection change in sourceFile.
function sourceFile_Callback(hObject, eventdata, handles)
% hObject    handle to sourceFile (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns sourceFile contents as cell array
%        contents{get(hObject,'Value')} returns selected item from sourceFile
refreshImages(handles)

% --- Executes during object creation, after setting all properties.
function sourceFile_CreateFcn(hObject, eventdata, handles)
% hObject    handle to sourceFile (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on slider movement.
function f_Callback(hObject, eventdata, handles)
% hObject    handle to f (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
refreshImages(handles)


% --- Executes during object creation, after setting all properties.
function f_CreateFcn(hObject, eventdata, handles)
% hObject    handle to f (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on slider movement.
function scale_Callback(hObject, eventdata, handles)
% hObject    handle to scale (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
refreshImages(handles)

% --- Executes during object creation, after setting all properties.
function scale_CreateFcn(hObject, eventdata, handles)
% hObject    handle to scale (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on slider movement.
function size_Callback(hObject, eventdata, handles)
% hObject    handle to size (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
refreshImages(handles)

% --- Executes during object creation, after setting all properties.
function size_CreateFcn(hObject, eventdata, handles)
% hObject    handle to size (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end
