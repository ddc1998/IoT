 var UserX = 320 , UserY = 240;
 $(function(){
        csmapi.set_endpoint ('http://140.113.199.200:9999');
        var profile = {
		    'dm_name': 'Maggie',          
			'idf_list':[maggiei],
			'odf_list':[maggieo],			
        };
		
        function maggiei(){
            return Math.random();
        }
        
        

        function maggieo(data){
            UserX = UserX + data[0][0]*10;
            UserY = UserY + data[0][1]*10;   
        }
      
/*******************************************************************/                
        function ida_init(){
            console.log(profile.d_name);
        }
        var ida = {
            'ida_init': ida_init,
        }; 
        dai(profile,ida);     
});
