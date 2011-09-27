$(document).ready(function(){
  var project = new function(){
    var self = this;
    this.id = null;
    this.rootNode = null;
    this.doc = null;
    this.dirty = false;
    this.onOpenedDeferred = $.Deferred();
    this.onOpened = this.onOpenedDeferred.promise();
    var createTaskLi = function(id){
      $('<li>', {
        class: 'ui-state-default',
        text: self.doc.snapshot['task:' + id + ':description']
      }).data('taskId', id).appendTo('.pile');
    };
    this.handleChange = function(op){
      if (op) {
        for (var i in op) {
          if (op[i].p[0] == 'tasks') {
            if (typeof op[i].li !== 'undefined') {
              // created new task
              createTaskLi(op[i].li);
            }

            if (typeof op[i].lm != 'undefined') {
              // sorted the list
              var findTaskLi = function(tid){
                var ret = null;
                $('.pile li').each(function(){
                  var li = $(this);
                  if (li.data('taskId') == tid){
                    ret = li;
                  }
                });
                return ret;
              };
              var li = findTaskLi(self.doc.snapshot.tasks[op[i].lm]);
              var occupant = $('.pile li').eq(op[i].lm);

              // actually move the item if it's not already in the right place
              if (li.data('taskId') !== occupant.data('taskId')) {
                if (occupant.index() >= li.index()) {
                  occupant.after(li);
                } else {
                  occupant.before(li);
                }
              }
            }
          }
        }
      }
      self.dirtyOff();
    };
    this.initialize = function(){
      // brand new project, initialize display
      for (var i in self.doc.snapshot.tasks) {
        var id = self.doc.snapshot.tasks[i];
        createTaskLi(id);
      }
    };
    this.template = {
      schema: 1,
      description: '',
      tasks: []
    };
    this.dirtyOn = function(){
      self.dirty = true;
      self.indicateDirtiness();
    };
    this.dirtyOff = function(){
      self.dirty = false;
      self.indicateDirtiness();
    };
    this.indicateDirtiness = function(){
      // toggle some visual dirtiness indicator
    };
    this.open = function(rootNode, pid){
      self.rootNode = rootNode;
      self.id = pid;
      sharejs.open(rootNode.data('projectPath'),
        sharejs.types.json,
        self.rootNode.data('sharejsUrl'),
        function(doc, error){

        self.doc = doc;
        self.doc.on('change', self.handleChange);
        if (self.doc.created) {
          // create a new project from the template
          doc.submitOp({p:[],od:null,oi:self.template});
        } else {
          self.initialize();
        }
      });
      self.rootNode.find('form').submit(function(){
        self.addTask($(this).serializeArray());
        return false;
      });
      self.onOpenedDeferred.resolve();
    };
    self.addTask = function(params){
      var tid = (new Date).getTime();
      var description = "";
      $(params).each(function(){
        if (this.name == 'description') {
          description = this.value;
        }
      });
      self.doc.submitOp([
        { p: ['tasks', self.doc.snapshot.tasks.length], li: tid },
        { p: ['task:' + tid + ':description'], oi: '' },
        { p: ['task:' + tid + ':description', 0], si: description }
      ]);
    };
  };

  var task = new function(){
    var self = this;
    this.id = null;
    this.open = function(tid){
      self.id = tid;
      var o = function(){
        $('.project-detail').hide();
        $('.task-detail').show();
        // open the task
      }

      // make sure the project is open
      if (!project.id){
        project.onOpened.done(o);
      } else {
        o();
      }
    };
    this.close = function(){
      $('.project-detail').show();
      $('.task-detail').hide();
    };
  };

  // If there is a project, then open it
  $(".project-detail").each(function(){
    project.open($(this));
  });

  // Buttonize the buttons
  $('nav a').button();
  $('.actions input').button();

  // Add the visual feedback onHover
  $(".pile li").live('hover', function(){
    $(this).toggleClass('ui-state-hover');
  });

  // Bind click handlers for task selection
  $(".pile li").live('click', function(){
    var li = $(this);
    li.toggleClass('ui-state-active')
      .siblings('li').removeClass('ui-state-active');
    var a = li.find('a');
    if (li.hasClass('ui-state-active')) {
      var tid = li.data('taskid');
      task.open(tid);
      window.history.pushState({
        selectedTaskId: tid
      }, "", a.attr('href'));
    } else {
      task.close();
      window.history.pushState({
        selectedTaskId: null
      }, "", a.closest('ul').data('project'));
    }
  });

  // Setup the sortable, and bind interesting events
  $(".pile").sortable({
    placeholder: "ui-state-highlight",
    start: function(event, ui){
      ui.item.originalIndex = ui.item.index();
    },
    update: function(event, ui){
      var newIndex = ui.item.index();
      project.doc.submitOp({
        p: ['tasks', ui.item.originalIndex],
        lm: newIndex
      });
    }
  });

  // Handle pop states
  window.onpopstate = function(event){
    if (event.state) { // popped a state
      $('.pile').find('li').removeClass('ui-state-active');
      if (event.state.selectedTaskId === null) {
        task.close();
      } else {
        $('.pile')
          .find('[data-taskId=' + event.state.selectedTaskId + ']')
          .addClass('ui-state-active');
        task.open(event.state.selectedTaskId);
      }
    } else { // no pushState, just a regular page load
      var activeLi = $('.pile').find('li.ui-state-active');
      if (activeLi.length) {
        task.open(activeLi.data('taskid'));
      } else {
        task.close();
      }
    }
  };

});
