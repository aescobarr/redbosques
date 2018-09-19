$(document).ready(function() {



});


$('tr.lv1').on("click", function(){

    var classLvl = this.className;
    console.log(classLvl);

    if(classLvl == "lv1 lv1Nat"){
        $('.lv2Nat').toggle();
    }else if(classLvl == "lv1 lv1Hh"){
        $('.lv2Hh').toggle();
    }else if(classLvl == "lv1 lv1Ie"){
        $('.lv2Ie').toggle();
    }

    /*if(classLvl == "lv1 lv1Nat"){
        $('.lv2Nat, .lv3Nat').toggle();
    }else if(classLvl == "lv1 lv1Hh"){
        $('.lv2Hh, .lv3Hh').toggle();
    }else if(classLvl == "lv1 lv1Ie"){
        $('.lv2Ie, .lv3Ie').toggle();
    }*/

    var validation = $('.lv2Nat').css("display");

    if(($('.lv2Nat').css("display")) == "none"){
        $('.lv3Nat').hide();
    }

    if(($('.lv2Hh').css("display")) == "none"){
        $('.lv3Hh').hide();
    }
});

$('tr.lv2').on("click", function(){

    var classLvl2 = this.className;
    console.log(classLvl2);

    if(classLvl2 == "lv2 lv2Nat"){
        $('.lv3Nat').toggle();
    }else if(classLvl2 == "lv2 lv2Hh"){
        $('.lv3Hh').toggle();
    }


    /*if(classLvl2 == "lv2 lv2Nat compo"){
        $('.lv3Nat.compo').toggle();
    }else if(classLvl2 == "lv2 lv2Nat compl"){
        $('.lv3Nat.compl').toggle();
    }else if(classLvl2 == "lv2 lv2Nat mad"){
        $('.lv3Nat.mad').toggle();
    }else if(classLvl2 == "lv2 lv2Nat micro"){
        $('.lv3Nat.micro').toggle();
     }else if(classLvl2 == "lv2 lv2Nat din"){
        $('.lv3Nat.din').toggle();
    }else if(classLvl2 == "lv2 lv2Hh ant"){
        $('.lv3Hh.ant').toggle();
    }else if(classLvl2 == "lv2 lv2Hh rec"){
        $('.lv3Hh.rec').toggle();
    }



    */

});
