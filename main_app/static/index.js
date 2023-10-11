let wy_input = null;
let pmc_input = []

const pmc_input_ele = document.querySelector('.pmc_input')
const onePreviewEle = document.querySelector('.one .preview');


// refresh previewEle when pmc_input[0] and pmc_input[1] are not null
function refreshOnePreviewEle() {
    onePreviewEle.style['display'] = 'block';

    const video1 = onePreviewEle.children[1].children[0];
    const video2 = onePreviewEle.children[1].children[1];

    // revoke video src
    URL.revokeObjectURL(video1.src);
    URL.revokeObjectURL(video2.src);

    // set video src
    video1.src = URL.createObjectURL(pmc_input[0]);
    video2.src = URL.createObjectURL(pmc_input[1]);
}


//if coach change, change pmc_input[0]
const coach_radios = document.querySelectorAll('input[name="coach_video"]');
coach_radios.forEach(radio => {
    radio.addEventListener('change', async (e) => {
        const selectedVideoValue = e.target.value;
        const selectedVideoElement = document.getElementById(selectedVideoValue);
        const selectedVideoSrc = selectedVideoElement.src;
        const response = await fetch(selectedVideoSrc);
        const videoBlob = await response.blob();
        const videoFile = new File([videoBlob], selectedVideoSrc.split('/').pop(), { type: videoBlob.type });
        pmc_input[0] = videoFile;
        console.log(pmc_input);
        // if pmc_input[1] is not null, refresh previewEle
        if (pmc_input[1]) {
            refreshOnePreviewEle();
        }
    });
});


pmc_input_ele.addEventListener('change', async (e) => {
    // pmc_input = []
    onePreviewEle.style['display'] = 'none';

    if (e.target.files.length === 0) {
        return
    }

    pmc_input[1] = e.target.files[0];
    //pmc_input.push(e.target.files[1]);

    if (pmc_input[0]) {
        refreshOnePreviewEle();
    }

    console.log(pmc_input)
})

const pmc_btn_ele = document.querySelector('.pmc_btn')
pmc_btn_ele.addEventListener('click', async (e) => {
    if (pmc_input.length === 0) {
        alert('没有选择文件')
        return
    }

    // if pmc_input[0] don't contain coach video, alert
    if (!pmc_input[0]) {
        alert('没有选择教练视频')
        return
    }
    if (!pmc_input[1]) {
        alert('没有上传学员视频')
        return
    }
    pmc_btn_ele.disabled = true
    pmc_btn_ele.style.backgroundColor = 'gray'

    try {
        const formdata = new FormData()
        formdata.append('files', pmc_input[0])
        formdata.append('files', pmc_input[1])
        alert('提交成功！正在处理，请稍等')

        var barcontent = document.getElementById("BarContent")
        barcontent.style['display'] = 'block'

        var id
        var elem = document.getElementById("myBar");
        var width = 0;
        id = setInterval(frame, 7000);
        async function frame() {
            console.log(width)
            if (width >= 100) {
                console.log("进入100")
                clearInterval(id);
                document.getElementById("myP").className = "w3-text-green w3-animate-opacity";
                document.getElementById("myP").innerHTML = "处理成功";
            } else {
                const state_res = await axios(
                    {
                        method: 'post',
                        url: `/get_state_pmc`,
                        data: formdata,
                        headers: {
                            'Content-Type': 'multipart/form-data',
                        },
                    }
                )
                console.log(state_res)
                text = state_res.data.text
                per = state_res.data.per
                width = per
                elem.style.width = width + '%'
                document.getElementById("myP").innerHTML = text

            }
        }

        const res = await axios(
            {
                method: 'post',
                url: `/upload_pmc`,
                data: formdata,
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            }
        )

        //成功
        console.log(res)
        if (res.data.state === 'success') {
            const result_ele = document.querySelector('.one .result')
            result_ele.style['display'] = 'block'
            const img1 = result_ele.children[1]
            const img2 = result_ele.children[2]
            const video = result_ele.children[3]

            //排序图片

            //const tmp1 = res.data.img1_urls.slice(2, 5)
            //res.data.img1_urls.splice(2, 3)
            //for (let ele of tmp1) {
            //    res.data.img1_urls.push(ele)
            //}
            //const tmp2 = res.data.img2_urls.slice(2, 5)
            //res.data.img2_urls.splice(2, 3)
            //for (let ele of tmp2) {
            //    res.data.img2_urls.push(ele)
            //}

            for (let i = 0; i < img1.children.length; i++) {
                img1.children[i].src = res.data.img1_urls[i]
            }
            for (let i = 0; i < img2.children.length; i++) {
                img2.children[i].src = res.data.img2_urls[i]
            }
            for (let i = 0; i < video.children.length; i++) {
                video.children[i].src = res.data.video_urls[i]
            }

        }
    }
    catch (err) {
        console.log(err);
    }
})

const wy_input_ele = document.querySelector('.wy_input')
wy_input_ele.addEventListener('change', async (e) => {
    wy_input = null
    document.querySelector('.two .preview').style['display'] = 'none'

    if (e.target.files.length === 0) {
        return
    }
    wy_input = e.target.files[0]

    //preview
    const preview_ele = document.querySelector('.two .preview')
    preview_ele.style['display'] = 'block'
    const video = preview_ele.children[1].children[0]
    const reader = new FileReader();
    reader.readAsDataURL(wy_input);
    reader.onload = async function () {
        video.src = reader.result
    }

    console.log(wy_input)
})

const wy_btn_ele = document.querySelector('.wy_btn')
wy_btn_ele.addEventListener('click', async (e) => {
    if (wy_input === null) {
        alert('没有选择文件')
        return
    }

    wy_btn_ele.disabled = true
    wy_btn_ele.style.backgroundColor = 'gray'

    const state_res = await axios(
                    {
                        method: 'post',
                        url: `/rm_state_wy`,
                        data: null,
                        headers: {
                            'Content-Type': 'multipart/form-data',
                        },
                    }
                )

    try {
        const formdata = new FormData()
        formdata.append('file', wy_input)
        alert('提交成功！正在处理，请稍等')

        var barcontent = document.getElementById("BarContent_wy")
        barcontent.style['display'] = 'block'

        var id
        var elem = document.getElementById("myBar_wy");
        var width = 0;
        id = setInterval(frame, 7000);
        async function frame() {
            console.log(width)
            if (width >= 100) {
                console.log("进入100")
                clearInterval(id);
                document.getElementById("myP_wy").className = "w3-text-green w3-animate-opacity";
                document.getElementById("myP_wy").innerHTML = "处理成功";
            } else {
                const state_res = await axios(
                    {
                        method: 'post',
                        url: `/get_state_wy`,
                        data: formdata,
                        headers: {
                            'Content-Type': 'multipart/form-data',
                        },
                    }
                )
                console.log(state_res)
                text = state_res.data.text
                per = state_res.data.per
                width = per
                elem.style.width = width + '%'
                document.getElementById("myP_wy").innerHTML = text

            }
        }

        const res = await axios(
            {
                method: 'post',
                url: `/upload_wy`,
                data: formdata,
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            }
        )

        //成功
        console.log(res)
        if (res.data.state === 'success') {
            const result_ele = document.querySelector('.two .result')
            result_ele.style['display'] = 'block'
            document.getElementById('wy_v1').src = res.data.urls[0]
            document.getElementById('wy_v2').src = res.data.urls[1]

            // video1.src = res.data.urls[0]
            // video2.src = res.data.urls[1]

            // for (let i = 0; i < video.children.length; i++) {
            //     video.children[i].src = res.data.urls[i]
            // }

        }
    }
    catch (err) {
        console.log(err);
    }
})


//切换tab
let active_tab = document.querySelector('.nav ul li:nth-of-type(1)')
const tabs = document.querySelectorAll('.nav ul li')
for (let i = 0; i < tabs.length; i++) {
    const ele = tabs[i];
    ((i, ele) => {
        ele.addEventListener('click', (e) => {
            active_tab.classList.remove('active')
            e.target.classList.add('active')
            active_tab = e.target
            if (i === 0) {
                document.querySelector('.one').style['display'] = 'block'
                document.querySelector('.two').style['display'] = 'none'
            } else {
                document.querySelector('.one').style['display'] = 'none'
                document.querySelector('.two').style['display'] = 'block'
            }
        })

    })(i, ele)
}

//下载功能
const wy_downloads = document.querySelectorAll('.wy_download_btn')
for (let i = 0; i < wy_downloads.length; i++) {
    const ele = wy_downloads[i];
    ((i, ele) => {
        ele.addEventListener('click', (e) => {
            const videos = document.querySelector('.two .result .video')
            const src = videos.children[i].src;
            (async (file) => {
                const response = await axios({
                    url: `${file}`,
                    method: "GET",
                    responseType: "blob",
                });
                return {
                    name: file,
                    content: response.data,
                };
            })(src).then((fileData) => {
                const fileUrl = URL.createObjectURL(fileData.content);
                const link = document.createElement("a");
                link.href = fileUrl;
                link.setAttribute("download", fileData.name);
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            });
        })
    })(i, ele)
}

document.querySelector('.pmc_download_btn').addEventListener('click', (e) => {
    const videos = document.querySelector('.one .result .video')
    const src = videos.children[0].src;
    (async (file) => {
        const response = await axios({
            url: `${file}`,
            method: "GET",
            responseType: "blob",
        });
        return {
            name: file,
            content: response.data,
        };
    })(src).then((fileData) => {
        const fileUrl = URL.createObjectURL(fileData.content);
        const link = document.createElement("a");
        link.href = fileUrl;
        link.setAttribute("download", fileData.name);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
})
