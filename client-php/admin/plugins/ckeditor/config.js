CKEDITOR.editorConfig = function( config )
{
config.toolbar = 'Full';

	config.scayt_autoStartup = false;
	config.filebrowserWindowWidth = '700';
    config.filebrowserWindowHeight = '500';
    config.enterMode = CKEDITOR.ENTER_BR;
    
    config.extraPlugins = 'more';

    config.toolbar_Full =
    [

    ['Bold','Italic'],
    ['NumberedList','BulletedList'],
    ['JustifyLeft','JustifyCenter','JustifyRight'],
    ['Link'],
    ['Image'],['HorizontalRule'],
    ['Format'],
    ['TextColor'],
    ['Table'],['Maximize'],['Source']
    ];
};
