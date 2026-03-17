<component>
  use App from runes;

  function (
    props => <div Design>, 
    design => 
      { 
        new App 
          { 
            runes: { 
              Design: design, 
              added: () => _.addError 
            } 
          }
          .run 
          .show 
      }
    )
end