// KindEditor.ready(function(K) {
//     window.editor = K.create('#id_body',{
//
//         // 指定大小
//         width:'800px',
//         height:'200px'
//     });
// });

KindEditor.ready(function(K) {
        K.create('textarea[name=body]',{
            width:750,
            height:200,
            uploadJson: '/admin/upload/kindeditor'
        });
});