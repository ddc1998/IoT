 $(function(){
        csmapi.set_endpoint ('http://140.113.199.200:9999');
        var profile = {
            'dm_name': 'Bulb',          
            'idf_list':[],
            'odf_list':[Color_O,Luminance]          
        };
        
        var r = 255 ;
        var g = 255;
        var b = 0;
        var lum = 100;
        var rr,gg,bb;

        function draw () {
            rr = Math.floor((r * lum) / 100);
            gg = Math.floor((g * lum) / 100);
            bb = Math.floor((b * lum) / 100);
        }   

        function Controller(){
            return Math.random();
        }

        function Color_O(data){
            r = data[0];
            g = data[1];
            b = data[2];
            $('.bulb-top, .bulb-middle-1, .bulb-middle-2, .bulb-middle-3, .bulb-bottom, .night').css(
                {'background': 'rgb('+ rr +', '+ gg +', '+ bb +')'}
            );
            draw();
        }
      
        function Luminance(data){
            lum = data[0]*10;
            draw();
        }
/*******************************************************************/                
        function ida_init(){
            console.log(profile.d_name);
            $('.bulbname')[0].innerText=profile.d_name
        }
        var ida = {
            'ida_init': ida_init,
        }; 
        dai(profile,ida);     
});
