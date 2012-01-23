CKEDITOR.plugins.add('more',
{
    init: function(editor)
    {
        var pluginName = 'more';
        editor.addCommand(pluginName, {
                        exec : function()
                        {
                                editor.fire( 'paste', { 'html' : '##more##' } );
                        }
                    });
                        
        editor.ui.addButton('More',
            {
                label: 'Add read more button',
                command: pluginName,
                icon: this.path + 'more.png'
            });
    }
});

